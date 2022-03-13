
## Base package

- this project created for base of tools and utils in data team.


### References

- [Setup package] https://towardsdatascience.com/create-your-custom-python-package-that-you-can-pip-install-from-your-git-repository-f90465867893

### Environemnt setup 
You have to set up this environment variables.
```bash
APP_NAME=candlestick
#------------------------------
#|        Kafka Config        |
#------------------------------
KAFKA_BOOTSTRAP_SERVERS=127.0.0.1:9092
KAFKA_MAX_POLL_RECORDS=1
KAFKA_AUTO_OFFSET_RESET=latest
KAFKA_ENABLE_AUTO_COMMIT=True
KAFKA_SESSION_TIMEOUT_MS=10000
KAFKA_CONNECTIONS_MAX_IDLE_MS=10000
KAFKA_CONNECTOR_URL=http://127.0.0.1:8083
KAFKA_SCHEMA_REGISTRY_URL=http://127.0.0.1:8081
KAFKA_TOPIC_AUTO_OFFSET_RESET=earliest
KAFKA_TOPIC_NUM_PARTITIONS=3
KAFKA_TOPIC_REPLICATION_FACTOR=3
KAFKA_TOPIC_RETENTION_TIME=2592000000
KAFKA_TOPIC_CLEANUP_POLICY=delete#valid values= [compact, delete]
#------------------------------
#|        TimescaleDB Config  |
#------------------------------
TIMESCALEDB_GENERAL_HOST=127.0.0.1
TIMESCALEDB_GENERAL_PORT=5432
TIMESCALEDB_GENERAL_USERNAME=admin
TIMESCALEDB_GENERAL_PASSWORD=*

#------------------------------
#|       Logger Config        |
#------------------------------
# Format string | json
LEVEL=noset
FORMAT=json
#------------------------------
#|       Proxy Config        |
#------------------------------
PROXY_HTTPS=http://127.0.0.1:8080
PROXY_HTTP=http://127.0.0.1:8080```
