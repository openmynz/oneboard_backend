import mysql.connector
import logging
import argparse
import asyncio
import schedule
import time

class MySQLReplicationSetup:
    def __init__(self, master_config, replicas_config):
        self.master_config = master_config
        self.replicas_config = replicas_config
        self.logger = self.setup_logger()

    def setup_logger(self):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        logger = logging.getLogger(__name__)
        return logger

    async def connect_to_mysql(self, config):
        try:
            connection = await asyncio.to_thread(mysql.connector.connect, **config)
            return connection
        except mysql.connector.Error as err:
            self.logger.error(f"Error connecting to MySQL: {err}")
            raise

    async def execute_sql(self, connection, cursor, sql):
        try:
            await asyncio.to_thread(cursor.execute, sql)
            return await asyncio.to_thread(cursor.fetchall)
        except mysql.connector.Error as err:
            self.logger.error(f"Error executing SQL query: {err}")
            raise

    async def setup_master(self):
        master_conn = await self.connect_to_mysql(self.master_config)
        master_cursor = master_conn.cursor()

        try:
            await self.execute_sql(master_conn, master_cursor, "CREATE USER 'repl'@'%' IDENTIFIED BY '<your_password>'")
            await self.execute_sql(master_conn, master_cursor, "GRANT REPLICATION SLAVE ON *.* TO 'repl'@'%'")
            await self.execute_sql(master_conn, master_cursor, "FLUSH PRIVILEGES")
            await self.execute_sql(master_conn, master_cursor, "FLUSH TABLES WITH READ LOCK")

            master_status = await self.execute_sql(master_conn, master_cursor, "SHOW MASTER STATUS")
            master_status = master_status[0] if master_status else None

        finally:
            await self.execute_sql(master_conn, master_cursor, "UNLOCK TABLES")
            master_cursor.close()
            master_conn.close()

        return master_status

    async def setup_replica(self, replica_config, master_status):
        replica_conn = await self.connect_to_mysql(replica_config)
        replica_cursor = replica_conn.cursor()

        try:
            await self.execute_sql(replica_conn, replica_cursor, f"CHANGE MASTER TO "
                                                                 f"MASTER_HOST='{self.master_config['host']}', "
                                                                 f"MASTER_USER='repl', MASTER_PASSWORD='<your_password>', "
                                                                 f"MASTER_LOG_FILE='{master_status[0]}', MASTER_LOG_POS={master_status[1]}")
            await self.execute_sql(replica_conn, replica_cursor, "START SLAVE")

        finally:
            replica_cursor.close()
            replica_conn.close()

    async def setup_replication(self):
        master_status = await self.setup_master()
        if master_status:
            self.logger.info("Master setup complete. Master status: %s", master_status)

            tasks = []
            for replica_config in self.replicas_config:
                task = self.setup_replica(replica_config, master_status)
                tasks.append(task)

            await asyncio.gather(*tasks)

            self.logger.info("Replication setup complete for all replicas. Replication started.")

def parse_arguments():
    parser = argparse.ArgumentParser(description='Set up MySQL master-slave replication.')
    parser.add_argument('--master-host', required=True, help='Hostname or IP address of the master server.')
    parser.add_argument('--master-user', default='root', help='Master server username. Default is "root".')
    parser.add_argument('--master-password', required=True, help='Master server password.')
    parser.add_argument('--replica-hosts', nargs='+', required=True, help='List of replica hostnames or IP addresses.')
    parser.add_argument('--replica-user', default='root', help='Replica server username. Default is "root".')
    parser.add_argument('--replica-passwords', nargs='+', required=True, help='List of replica server passwords.')
    parser.add_argument('--interval', type=int, default=3600, help='Interval in seconds to run the replication setup. Default is 1 hour.')

    return parser.parse_args()

async def main():
    args = parse_arguments()

    master_config = {
        'host': args.master_host,
        'user': args.master_user,
        'password': args.master_password,
    }

    replicas_config = [
        {
            'host': replica_host,
            'user': args.replica_user,
            'password': replica_password,
        }
        for replica_host, replica_password in zip(args.replica_hosts, args.replica_passwords)
    ]

    replication_setup = MySQLReplicationSetup(master_config, replicas_config)

    # Run replication setup at specified intervals
    schedule.every(args.interval).seconds.do(replication_setup.setup_replication)

    while True:
        await schedule.run_pending()
        await asyncio.sleep(1)

if __name__ == "__main__":
    asyncio.run(main())
