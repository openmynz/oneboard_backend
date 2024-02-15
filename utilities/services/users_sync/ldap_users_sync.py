import argparse
import logging
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES, SUBTREE
from retrying import retry
from constants import *

logging.basicConfig(level=logging.INFO)


class LDAPService:
    """_summary_"""

    def __init__(self, ldap_host, ldap_port, ldap_username, ldap_password):
        self.ldap_host = ldap_host
        self.ldap_port = ldap_port
        self.ldap_username = ldap_username
        self.ldap_password = ldap_password

    @retry(wait_random_min=1000, wait_random_max=3000, stop_max_attempt_number=3)
    def fetch_users_from_ldap(self):
        """_summary_

        Returns:
            _type_: _description_
        """
        server = Server(
            self.ldap_host, port=self.ldap_port, use_ssl=False, get_info=ALL
        )
        try:
            logging.info("Trying to connect to LDAP server")
            conn = Connection(
                server,
                user=self.ldap_username,
                password=self.ldap_password,
                auto_bind=True,
            )
            logging.info("Connection to LDAP server is successful")
            logging.info("Searching the ldap for user details")
            conn.search(
                search_base="ou=Users,ou=om,dc=omz,dc=com",
                search_filter="(objectClass=person)",
                search_scope=SUBTREE,
                attributes=ALL_ATTRIBUTES,
            )
            logging.info("Search query to LDAP server was successful.")

            users = self.parse_ldap_response_to_build_user_dict(conn.entries)
            return users
        except Exception as e:
            logging.error(f"Error while fetching users from LDAP: {e}")
            raise

    def parse_ldap_response_to_build_user_dict(self, data):
        result = []
        for entry in data:
            temp = {}
            temp["dn"] = entry.distinguishedName.value
            temp["fname"] = entry.givenName.value
            try:
                temp["lname"] = entry.sn.value
            except Exception as e:
                temp["lname"] = ""
            temp["cn"] = entry.cn.value
            temp["accountname"] = entry.sAMAccountName.value
            result.append(temp)

        return result


class SyncUsers:
    def __init__(self, host, port, username, password, users_endpoint) -> None:
        self.api_ip = host
        self.port = port
        self.username = username
        self.password = password
        self.users_endpoint = users_endpoint

    def get_available_users_from_db(self):
        pass

    def create_user(self):
        pass

    def delete_user(self):
        pass


def main():
    parser = argparse.ArgumentParser(
        description="Fetch LDAP users and sync them with a database"
    )
    parser.add_argument("--ldap-host", default=LDAP_DEFAULT_HOST, help="LDAP host")
    parser.add_argument(
        "--ldap-port", type=int, default=LDAP_DEFAULT_PORT, help="LDAP port"
    )
    parser.add_argument(
        "--ldap-username", default=LDAP_DEFAULT_USERNAME, help="LDAP username"
    )
    parser.add_argument(
        "--ldap-password", default=LDAP_DEFAULT_PASSWORD, help="LDAP password"
    )
    parser.add_argument("--api-host", default=API_DEFAULT_HOST, help="api host")
    parser.add_argument(
        "--api-port", type=int, default=API_DEFAULT_PORT, help="api port"
    )
    parser.add_argument(
        "--api-username", default=API_DEFAULT_USERNAME, help="api username"
    )

    parser.add_argument(
        "--api-password", default=API_DEFAULT_PASSWORD, help="api password"
    )

    parser.add_argument(
        "--api-users-endpoint",
        default=API_DEFAULT_USERSENDPOINT,
        help="Users end point",
    )
    args = parser.parse_args()

    # Initialize services
    ldap_service = LDAPService(
        args.ldap_host, args.ldap_port, args.ldap_username, args.ldap_password
    )

    try:
        # Fetch users from LDAP
        users = ldap_service.fetch_users_from_ldap()
        print(users)

        db_users = []

        logging.info("Sync completed successfully!")
    except Exception as e:
        logging.error(f"An error occurred during sync: {e}")


if __name__ == "__main__":
    main()
