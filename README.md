# AC51041-RestAPI
Rest API for AC51041 assignment

# AC51041
Micro Services based VOD service
*This repo also acts as the central ReadMe for this project*


### A Warning
**Don't copy this repo for you're assigment**, this is not a good example of what to do and is more 
overcomplicated than this should be to get the same result. Also don't use this example in production.

You really should use Kubernetes and something like Terraform to handle defining your services in an actual production
environment along with something like [Vault](https://www.vaultproject.io/) to handle secrets.

## Accompanying Git Repos
- [Login Service](https://github.com/vlee489/AC51041-Login)
- [Film Catalogue Service](https://github.com/vlee489/AC51041-catalogue)
- [Front End Service](https://github.com/vlee489/AC51041-ui)
- [History and Personalization Service](https://github.com/vlee489/AC51041-Personalisation)
- [Key Pre-signing Service](https://github.com/vlee489/AC51041-signer)
- [REST API (This repo)](https://github.com/vlee489/AC51041-RestAPI)

## Systems used
- Docker
- Docker Compose
- MongoDB & Atlas Cloud Hosting
- Postgres
- Redis
- Digital Ocean Spaces / AWS S3
- RabbitMQ
- FastAPI
- OpenAPI / Swagger
- Python 3.11
- HTML/CSS/JS
- Video.js
- Msgpack
- GitHub Actions (As CI)
- Docker.io Registry

## Docker Setup
Use the files in the `/deploy` folder in this repo to deploy the docker stack

## Continuous Integration
All CI is using GitHub actions setup via `./github` folder, and results can be **viewed** via the actions tab on GitHub

### What this was for
This was made for a University of Dundee CompSci Devops Module.