# Docker Compose Deployment

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