# 1. Domínio de Contas (Clientes)
Responsável por:

Cadastro

Status

Elegibilidade

Adesão ao produto

Tabela:
```sql
accounts
---------
id
user_id
status
created_at
```

Aqui não existe tipo MASTER.

Porque isso é domínio do cliente.


# 2. Domínio do Produto (Top Five)

Aqui mora o conceito da conta master.

Ela não é uma “conta de cliente”.

Ela é um mecanismo operacional do produto.

Modelagem:

```sql
investment_products
-------------------
id
name
strategy_type
brokerage_id
```
```sql
product_operational_accounts
----------------------------
id
product_id
external_broker_account_code
```

Só existe uma? Sim.
Mas pertence ao produto.

Se amanhã existir:

Top Five Conservador

Top Five Agressivo

Você terá múltiplas contas operacionais.

A separação já estará correta.


# 3. Domínio de Portfólio / Custódia

Aqui você unifica de forma elegante:

```sql
portfolios
----------
id
owner_type (ACCOUNT | PRODUCT)
owner_id
```
```sql
positions
---------
portfolio_id
asset_id
quantity
```

Agora:

Conta cliente → tem portfolio

Produto → tem portfolio operacional

Sem duplicação.
Sem hierarquia falsa.
Sem if espalhado.

-----


# Clients

## Clients

| ID        | UUID v7     |
|-----------|-------------|
| Nome      | Varchar     |
| Email     | Varchar(64) |
| CPF       | Varchar(11) |
| IsActive  | Bool        |
| CreatedAt | Timestamp   |

# Accounts

## Accounts

| ID             | UUID v7             |
|----------------|---------------------|
| AccountNumber  | Varchar             |
| Type           | Enum(Master,Child)  |
| CreatedAt      | Timestamp           |

## ClientAccounts

| AccountId     | FK Accounts |
|---------------|-------------|
| ClientId      | FK Clients  |
| AccountStatus | Enum        |

## MasterAccounts

| AccountId     | FK Accounts |
|---------------|-------------|
| InternalCode  | Varchar     |

# No way

## ProductSubscription

| ID            | UUID v7                     |
|---------------|-----------------------------|
| AccountId     | FK Accounts                 |
| BasketId      | FK InvestmentBaskets        |
| MonthlyAmount | Decimal(18, 4)              |
| Status        | Enum(“Active”, “Cancelled”) |
| CreatedAt     | Timestamp                   |


# Products

## InvestmentProducts

| ID        | UUID v7              |
|-----------|----------------------|
| Name      | Varchar              |
| Ticker    | Varchar              |
| Type      | Enum(“stock”, “fii”) |
| CreatedAt | Timestamp            |

## InvestmentBaskets

| ID        | UUID v7   |
|-----------|-----------|
| Nome      | Varchar   |
| Active    | Bool      |
| CreatedAt | Timestamp |
| DeactivatedAt | Timestamp |

## BasketAssets

| ID         | UUID v7              |
|------------|----------------------|
| BasketId   | FK Baskets           |
| ProductId  | FK InvesmentProducts |
| Percentage | float8               |
| CreatedAt  | Timestamp            |


# Custody

## BulkOrders

| ID            | UUID v7                        |
|---------------|--------------------------------|
| ProductId     | FK InvesmentProducts           |
| TotalQuantity | Int16                          |
| TotalAmount   | Decimal(18, 4)                 |
| Status        | Enum(“Pending”, “Distributed”) |
| CreatedAt     | Timestamp                      |

## Positions

| ID           | UUID v7              |
|--------------|----------------------|
| ProductId    | FK InvesmentProducts |
| AccountId    | FK Accounts          |
| AveragePrice | Decimal(18, 4)       |
| Quantity     | Int16                |
| CreatedAt    | Timestamp            |

## OperationalResiduals

| ID               | UUID v7       |
|------------------|---------------|
| BulkOrderId      | FK BulkOrders |
| ResidualQuantity | Int16         |
| CreatedAt        | Timestamp     |

## TransactionHistory

| Campo       | Tipo          | Descrição                                                                       |
|-------------|---------------|---------------------------------------------------------------------------------|
| ID          | UUID v7       | Identificador único da transação.                                               |
| AccountId   | FK Accounts   | De quem é essa movimentação.                                                    |
| ProductId   | FK Products   | Qual ativo foi comprado/vendido.                                                |
| BulkOrderId | FK BulkOrders | Chave de Ouro: Liga a transação do cliente à compra da Master (Auditabilidade). |
| Type        | Enum          | "BUY" (Compra) ou "SELL" (Venda).                                               |
| Quantity    | Int16         | Quantidade exata alocada para este cliente.                                     |
| UnitPrice   | Decimal(10,4) | Preço unitário da cota no momento da compra.                                    |
| TotalAmount | Decimal(18,4) | Valor total financeiro (Quantidade * Preço).                                    |
| CreatedAt   | Timestamp     | Data e hora exata da transação.                                                 |

