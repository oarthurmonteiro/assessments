namespace AutomatedInvestment.Domain.Accounts.Entities;

public enum AccountStatus
{
    Active = 1,
    Pending = 2,
    Cancelled = 3,
}

public class ClientAccount : Account
{
    public Guid ClientId { get; private set; }
    public Guid SubscriptionId { get; private set; }
    public AccountStatus Status { get; private set; }
    
    private ClientAccount() { } // Construtor para o EF

    public static ClientAccount Create(Guid clientId, Guid subscriptionId, string accountNumber)
    {
        return new ClientAccount
        {
            Id = Guid.CreateVersion7(),
            AccountNumber = accountNumber,
            Type = AccountType.Child,
            ClientId = clientId,
            SubscriptionId = subscriptionId,
            Status = AccountStatus.Active,
            CreatedAt = DateTime.UtcNow,
        };
    }
}