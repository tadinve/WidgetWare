import pandas as pd
from sqlalchemy import create_engine
from faker import Faker
from faker.providers import DynamicProvider, internet, date_time, user_agent, python

account_identifier = "<account_identifier>"
user = "<user_login_name>"
password = "<password>"
database_name = "<database_name>"
schema_name = "<schema_name>"
postgres_link = "postgresql://postgres:postgres@database-1.c3tdzmqqtx8o.us-east-2.rds.amazonaws.com/widgetware"


status_code_profider = DynamicProvider(
    provider_name="status_code",
    elements=[404, 500, 200, 201, 501],
)

content_type_profider = DynamicProvider(
    provider_name="content_type",
    elements=[
        "application/octet-stream",
        "application/xml",
        "text/*",
        "application/x-www-form-urlencoded",
    ],
)


def load_web_traffic_data():
    df = pd.DataFrame()
    
    fake = Faker()
    fake.add_provider(internet)
    fake.add_provider(date_time)
    fake.add_provider(user_agent)
    fake.add_provider(python)
    fake.add_provider(status_code_profider)

    for _ in range(10):
        row = {
            "host_name" : fake.hostname(),
            "host_ip" : fake.ipv4(),
            "timestamp" : fake.iso8601(),
            "client_info" : fake.user_agent(),
            "status_code" : fake.status_code(),
            "bytes_sent" : fake.pyint(min_value=10, max_value=1023),
            "url" : fake.url(),
            "user_log_name" : fake.user_name(),
            "authenticated_user" : fake.pybool(),
            "method" : fake.http_method(),
            "content_type" : fake.content_type(),
            "time_to_serve" : fake.pyint(min_value=10, max_value=100),
        }
        
        df.append(row, ignore_index=True)

    print(df.head())
    # postgres_engine = create_engine(postgres_link)
