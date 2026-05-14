# =============================
# Base SDK
# =============================
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS base


# =============================
# Development
# =============================
FROM base AS dev
WORKDIR /app
COPY . .

EXPOSE 5000

RUN dotnet restore
RUN dotnet tool restore

CMD ["dotnet", "run", "--project", "src/AutomatedInvestment.Api", "--urls=http://0.0.0.0:5000"]


# =============================
# Build (produção)
# =============================
FROM base AS build
WORKDIR /src
COPY . .
RUN dotnet publish src/AutoInvest.Api/AutoInvest.Api.csproj -c Release -o /app/out


# =============================
# Production Runtime
# =============================
FROM mcr.microsoft.com/dotnet/aspnet:8.0 AS prod
WORKDIR /app

COPY --from=build /app/out .
EXPOSE 8080

ENTRYPOINT ["dotnet", "AutoInvest.Api.dll"]