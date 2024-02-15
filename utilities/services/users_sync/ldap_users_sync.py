import argparse
import logging
import requests
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


class SyncUsersData:
    def __init__(self, host, port, username, password, users_endpoint) -> None:
        self.api_ip = host
        self.port = port
        self.username = username
        self.password = password
        self.users_endpoint = users_endpoint

    def get_available_users_from_db(self):
        print(self.users_endpoint)
        users = requests.get(
            url=self.users_endpoint, auth=(self.username, self.password)
        )
        return users.json()

    def create_user(self, data):
        try:
            status = requests.post(
                url=self.users_endpoint, data=data, auth=(self.username, self.password)
            )
            if status.response_code == 201:
                return True
            else:
                return False
        except Exception as e:
            print(f"Exception occured is : {e}")
        else:
            logging.info("User create successfully")
        finally:
            pass

    def delete_user(self, id):
        pass

    def sync(self, ldap_users_info: dict):
        # Fetch users from DB
        db_users = self.get_available_users_from_db()
        db_distinguished_names = []
        for db_user in db_users:
            db_distinguished_names.append(db_user["distinguished_name"])
        db_distinguished_names = set(db_distinguished_names)

        ldap_distinguished_names = []
        for ldap_user in ldap_users_info:
            ldap_distinguished_names.append(ldap_user["dn"])
            if ldap_user["dn"] in db_distinguished_names:
                pass
            else:
                data = {}
                data["distinguished_name"] = ldap_user["dn"]
                data["first_name"] = ldap_user["fname"]
                data["last_name"] = ldap_user["lname"]
                data["common_name"] = ldap_user["cn"]
                data["account_name"] = ldap_user["accountname"]
                self.create_user(data=data)
        ldap_distinguished_names = set(ldap_distinguished_names)

        for db_user in db_users:
            if db_users["distinguished_name"] in ldap_distinguished_names:
                pass
            else:
                # delete the users that are present in db but not present in ldap
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
        default=API_DEFAULT_LDAPUSERS_ENDPOINT,
        help="Users end point",
    )
    args = parser.parse_args()

    # Initialize services
    ldap_service = LDAPService(
        args.ldap_host, args.ldap_port, args.ldap_username, args.ldap_password
    )

    api_object = SyncUsersData(
        host=args.api_host,
        port=args.api_port,
        username=args.api_username,
        password=args.api_password,
        users_endpoint=args.api_users_endpoint,
    )
    try:
        # Fetch users from LDAP
        ldap_users = ldap_service.fetch_users_from_ldap()
        api_object.sync(ldap_users_info=ldap_users)

        logging.info("Sync completed successfully!")
    except Exception as e:
        logging.error(f"An error occurred during sync: {e}")


if __name__ == "__main__":
    main()
