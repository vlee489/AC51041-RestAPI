# Docker Compose Deployment

## Deployment
To deploy this project use an x86-64 or ARM64 (Apple Silicon/AWS Graviton/Ampere Altra) based server with
Docker and Docker Compose setup. You'll need to forward port `443` for the reverse proxy.

Make sure to edit the docker compose files to include you 2 TLDs for the RestAPI and UI along with an email for Let's Encrypt to
notify you on.

### Env
create the following `.env` files in the `.config/` folder for Docker Compose to use.

#### api.env
```dotenv
DEBUG=TRUE
MQURI=""  # RabitMQ
```

#### login.env
```dotenv
DEBUG=TRUE
REDIS=""  # Redis Database
DBURI=""  # SQL/Postgres Database
MQURI=""  # RabitMQ
```

#### catalogue.env
```dotenv
DEBUG=True
MONGOURI=""  # MongoDB URI
```

#### personalisation.env
```dotenv
DEBUG=True
MONGOURI=""  # MongoDB URI
```

#### signer.env
```dotenv
DEBUG=
MQURI=""
BUCKETREGION=""
BUCKETENDPOINT=""
BUCKETKEYID=""
BUKCETACCESSKEY=""
```

#### db.env
````dotenv
POSTGRES_PASSWORD=""
POSTGRES_USER=""
POSTGRES_DB=devops
````

#### proxy.env
```dotenv
CF_API_EMAIL=
CF_DNS_API_TOKEN=
CF_ZONE_API_TOKEN=
```