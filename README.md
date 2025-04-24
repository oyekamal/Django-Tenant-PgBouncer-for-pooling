# Django Multi-Tenant Application with PgBouncer

This project demonstrates a Django multi-tenant application using django-tenants with PgBouncer for connection pooling. The application uses a PostgreSQL database and Docker for containerization.

## Architecture Overview

The project consists of three main services:
- **PostgreSQL**: Main database server
- **PgBouncer**: Connection pooling service
- **Django Web Application**: Multi-tenant application using django-tenants

### Why PgBouncer with Multi-Tenancy?

Django's multi-tenant setup (django-tenants) doesn't provide connection pooling out of the box. This can lead to several issues:

1. **Connection Overhead**: Each tenant request creates a new database connection, which is resource-intensive
2. **Connection Limits**: PostgreSQL has limits on maximum connections (default: 100)
3. **Performance Impact**: Creating new connections for each request increases response time

PgBouncer solves these issues by:
- Maintaining a pool of connections that can be reused
- Reducing the number of actual PostgreSQL connections
- Improving response times by eliminating connection overhead
- Managing connection limits effectively across all tenants

## Prerequisites

- Docker
- Docker Compose
- Python 3.9+

## Project Setup

1. Clone the repository:
```bash
git clone https://github.com/oyekamal/Django-Tenant-PgBouncer-for-pooling.git
cd Django-Tenant-PgBouncer-for-pooling
```

2. Build and start the containers:
```bash
docker-compose up --build
```

This will:
- Start PostgreSQL database
- Configure PgBouncer
- Run Django migrations
- Create the public tenant
- Create a default superuser

## Managing Tenants

### Creating a New Tenant

Use the management command:

```bash
# Basic usage
docker-compose exec web python manage.py create_tenant \
    --schema_name=customer1 \
    --name="Customer One" \
    --domain=customer1.localhost

# Advanced usage
docker-compose exec web python manage.py create_tenant \
    --schema_name=customer1 \
    --name="Customer One" \
    --domain=customer1.localhost \
    --paid_until=2024-12-31 \
    --on_trial=false
```

Parameters:
- `schema_name`: Unique identifier for the tenant (required)
- `name`: Display name for the tenant (required)
- `domain`: Domain name for the tenant (required)
- `paid_until`: Subscription end date (optional, format: YYYY-MM-DD)
- `on_trial`: Trial status (optional, default: true)

### Creating a Superuser

For the public tenant:
```bash
docker-compose exec web python manage.py create_public_superuser
```

This creates a superuser with default credentials:
- Username: admin
- Email: admin@example.com
- Password: admin123

Custom credentials:
```bash
docker-compose exec web python manage.py create_public_superuser \
    --username=myuser \
    --email=myuser@example.com \
    --password=mypassword
```

## Configuration Details

### PgBouncer Configuration

PgBouncer is configured in `pgbouncer/pgbouncer.ini`:
- Pool Mode: transaction
- Max Client Connections: 100
- Default Pool Size: 20
- Authentication Type: md5

### Database Configuration

PostgreSQL settings in `docker-compose.yml`:
- Database: tenant_db
- User: tenant_user
- Password: tenant_pass
- Port: 5432 (internal), 6432 (PgBouncer)

### Django Settings

Key settings in `config/settings.py`:
- PUBLIC_SCHEMA_NAME = 'public'
- TENANT_MODEL = "core.Client"
- TENANT_DOMAIN_MODEL = "core.Domain"

## Development Workflow

1. Create a new tenant
2. Access tenant-specific admin at: `http://<tenant-domain>/admin/`
3. Create tenant-specific data
4. Access public tenant at: `http://localhost:8000/admin/`

## Connection Pooling Details

PgBouncer manages connections with these settings:
- `pool_mode = transaction`: Connections are returned to the pool after each transaction
- `max_client_conn = 100`: Maximum simultaneous client connections
- `default_pool_size = 20`: Number of cached connections per user/database pair

Benefits:
1. **Resource Efficiency**: Fewer actual database connections
2. **Better Scaling**: Handle more tenants with limited database connections
3. **Improved Performance**: Reduced connection overhead
4. **Connection Management**: Prevent connection exhaustion

## Troubleshooting

1. If migrations fail:
```bash
docker-compose down -v  # Remove volumes
docker-compose up --build  # Rebuild with fresh DB
```

2. To check PgBouncer status:
```bash
docker-compose exec pgbouncer psql -p 6432 -U tenant_user pgbouncer
```

3. To view logs:
```bash
docker-compose logs web  # Django logs
docker-compose logs pgbouncer  # PgBouncer logs
docker-compose logs db  # PostgreSQL logs
```

## Security Considerations

1. Change default credentials in production
2. Configure proper SSL/TLS
3. Update PgBouncer and PostgreSQL security settings
4. Implement proper tenant isolation
5. Use strong passwords for tenant databases

## Production Deployment

Additional considerations for production:
1. Use environment variables for sensitive data
2. Configure proper backup strategy
3. Set up monitoring and logging
4. Configure SSL/TLS
5. Implement proper security measures
6. Scale PgBouncer and PostgreSQL appropriately

## License

[Your License Here]

## Contributing

[Your Contributing Guidelines Here]