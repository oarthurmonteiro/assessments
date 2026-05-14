```sh
docker run --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/app:/workspace \
  -w /workspace \
  mcr.microsoft.com/dotnet/sdk:8.0 \
  bash -c "\
    mkdir -p src && \
    dotnet new sln -n AutomatedInvestment && \
    cd src && \
    dotnet new webapi -n AutomatedInvestment.Api && \
    dotnet new worker -n AutomatedInvestment.Worker && \
    cd .. && \
    dotnet sln add src/AutomatedInvestment.Api/AutomatedInvestment.Api.csproj && \
    dotnet sln add src/AutomatedInvestment.Worker/AutomatedInvestment.Worker.csproj \
  "
```

🔥 Como criar os projetos

Dentro do container SDK ou local:

dotnet new classlib -n AutomatedInvestment.Domain -o src/AutomatedInvestment.Domain
dotnet new classlib -n AutomatedInvestment.Application -o src/AutomatedInvestment.Application
dotnet new classlib -n AutomatedInvestment.Infrastructure -o src/AutomatedInvestment.Infrastructure
dotnet new webapi -n AutomatedInvestment.Api -o src/AutomatedInvestment.Api --use-controllers
dotnet new worker -n AutomatedInvestment.Worker -o src/AutomatedInvestment.Worker
dotnet new xunit -n AutomatedInvestment.UnitTests -o tests/AutomatedInvestment.UnitTests
dotnet new xunit -n AutomatedInvestment.IntegrationTests -o tests/AutomatedInvestment.IntegrationTests

Adicionar na solution:

dotnet sln add $(find . -name "*.csproj")
🔗 Referências corretas

Domain

→ nenhuma

Application

→ referencia Domain

dotnet add src/AutomatedInvestment.Application reference src/AutomatedInvestment.Domain

Infrastructure

→ referencia Application + Domain

dotnet add src/AutomatedInvestment.Infrastructure reference src/AutomatedInvestment.Application
dotnet add src/AutomatedInvestment.Infrastructure reference src/AutomatedInvestment.Domain


API

→ referencia Application + Infrastructure

dotnet add src/AutomatedInvestment.Api reference src/AutomatedInvestment.Application
dotnet add src/AutomatedInvestment.Api reference src/AutomatedInvestment.Infrastructure

Worker

→ referencia Application + Infrastructure

dotnet add src/AutomatedInvestment.Worker reference src/AutomatedInvestment.Application
dotnet add src/AutomatedInvestment.Worker reference src/AutomatedInvestment.Infrastructure

🐬 Migrations (importante)

Execute sempre assim:

dotnet ef migrations add InitialCreate \
  --project src/AutomatedInvestment.Infrastructure \
  --startup-project src/AutomatedInvestment.Api

Assim:

Migration fica na Infrastructure

Configuração vem da API

🐳 Docker

Você deve ter dois Dockerfiles:

docker/api.Dockerfile
docker/worker.Dockerfile

E no compose:

services:
  api:
    build:
      context: .
      dockerfile: docker/api.Dockerfile

  worker:
    build:
      context: .
      dockerfile: docker/worker.Dockerfile

```sh
docker run --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}:/workspace \
  -w /workspace \
  mcr.microsoft.com/dotnet/sdk:8.0 \
  bash -c "\
    dotnet new sln -n AutomatedInvestment && \
    dotnet new classlib -n AutomatedInvestment.Domain -o src/AutomatedInvestment.Domain && \
    dotnet new classlib -n AutomatedInvestment.Application -o src/AutomatedInvestment.Application && \
    dotnet new classlib -n AutomatedInvestment.Infrastructure -o src/AutomatedInvestment.Infrastructure && \
    dotnet new webapi -n AutomatedInvestment.Api -o src/AutomatedInvestment.Api --use-controllers && \
    dotnet new worker -n AutomatedInvestment.Worker -o src/AutomatedInvestment.Worker && \
    dotnet new xunit -n AutomatedInvestment.UnitTests -o tests/AutomatedInvestment.UnitTests && \
    dotnet new xunit -n AutomatedInvestment.IntegrationTests -o tests/AutomatedInvestment.IntegrationTests
  "
```

```sh
docker run --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/app:/workspace \
  -w /workspace \
  mcr.microsoft.com/dotnet/sdk:10.0 \
  bash -c "dotnet sln add \$(find . -name '*.csproj')"
```

docker run --rm \
  -u $(id -u):$(id -g) \
  -v ${PWD}/app:/workspace \
  -w /workspace \
  mcr.microsoft.com/dotnet/sdk:10.0 \
  bash -c "\
  dotnet add src/AutomatedInvestment.Infrastructure package Microsoft.EntityFrameworkCore && \ 
dotnet add src/AutomatedInvestment.Infrastructure package Microsoft.EntityFrameworkCore.Design && \
dotnet add src/AutomatedInvestment.Infrastructure package Pomelo.EntityFrameworkCore.MySql \
"

docker compose run --rm api dotnet ef migrations add InitialCreate \
  --project src/AutomatedInvestment.Infrastructure \
  --startup-project src/AutomatedInvestment.Api

  docker compose run --rm api dotnet ef database update \
  --project src/AutomatedInvestment.Infrastructure \
  --startup-project src/AutomatedInvestment.Api