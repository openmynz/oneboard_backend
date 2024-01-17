import pymongo
import logging
import argparse
import asyncio
import schedule
import time

class MongoDBReplicationSetup:
    def __init__(self, primary_config, secondaries_config):
        self.primary_config = primary_config
        self.secondaries_config = secondaries_config
        self.logger = self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        return logger

    async def connect_to_mongodb(self, config):
        try:
            client = await asyncio.to_thread(pymongo.MongoClient, **config)
            return client
        except pymongo.errors.ConnectionFailure as err:
            self.logger.error(f"Error connecting to MongoDB: {err}")
            raise

    async def setup_primary(self):
        primary_client = await self.connect_to_mongodb(self.primary_config)

        try:
            # Check if primary is already configured as a replica set
            is_configured = await asyncio.to_thread(primary_client.admin.command, 'replSetGetStatus')
            if 'members' in is_configured:
                self.logger.info("Primary is already configured as a replica set.")
                return

            # Configure primary as a replica set
            config = {
                '_id': 'myReplicaSet',
                'members': [
                    {'_id': 0, 'host': f"{self.primary_config['host']}:{self.primary_config['port']}"},
                ]
            }
            await asyncio.to_thread(primary_client.admin.command, 'replSetInitiate', config)
            self.logger.info("Primary configured as a replica set.")

        finally:
            primary_client.close()

    async def setup_secondary(self, secondary_config, primary_host, primary_port):
        secondary_client = await self.connect_to_mongodb(secondary_config)

        try:
            # Add the secondary to the replica set
            await asyncio.to_thread(secondary_client.admin.command, 'replSetAdd', {'host': f"{primary_host}:{primary_port}"})
            self.logger.info("Secondary added to the replica set.")

        finally:
            secondary_client.close()

    async def setup_replication(self):
        await self.setup_primary()

        primary_host = self.primary_config['host']
        primary_port = self.primary_config['port']

        for secondary_config in self.secondaries_config:
            await self.setup_secondary(secondary_config, primary_host, primary_port)

    async def check_replication_status(self):
        client = await self.connect_to_mongodb(self.primary_config)

        try:
            status = await asyncio.to_thread(client.admin.command, 'replSetGetStatus')
            self.logger.info("Replication Status: %s", status)

        finally:
            client.close()

def parse_arguments():
    parser = argparse.ArgumentParser(description='Set up MongoDB replication.')
    parser.add_argument('--primary-host', required=True, help='Hostname or IP address of the primary MongoDB server.')
    parser.add_argument('--primary-port', type=int, default=27017, help='Port of the primary MongoDB server. Default is 27017.')
    parser.add_argument('--secondaries', nargs='+', required=True, help='List of secondary MongoDB server hostnames or IP addresses.')
    parser.add_argument('--interval', type=int, default=3600, help='Interval in seconds to run the replication setup. Default is 1 hour.')

    return parser.parse_args()

async def main():
    args = parse_arguments()

    primary_config = {
        'host': args.primary_host,
        'port': args.primary_port,
    }

    secondaries_config = [{'host': secondary_host, 'port': args.primary_port} for secondary_host in args.secondaries]

    replication_setup = MongoDBReplicationSetup(primary_config, secondaries_config)

    # Run replication setup at specified intervals
    schedule.every(args.interval).seconds.do(replication_setup.setup_replication)

    # Check replication status every 5 minutes
    schedule.every(5).minutes.do(replication_setup.check_replication_status)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
