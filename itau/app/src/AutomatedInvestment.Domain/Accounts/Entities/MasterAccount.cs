namespace AutomatedInvestment.Domain.Accounts.Entities;

public class MasterAccount : Account
{
    // Nome operacional para auditoria (ex: "RESIDUAL_TOP_FIVE_MARCO_2026")
    public string InternalCode { get; private set; } = null!;
    
    private MasterAccount() { } // Construtor para o EF

    public static MasterAccount Create(string internalCode)
    {
        return new MasterAccount
        {
            Id = Guid.CreateVersion7(),
            AccountNumber = $"MST-{Guid.NewGuid().ToString()[..8].ToUpper()}",
            Type = AccountType.Master,
            InternalCode = internalCode,
            CreatedAt = DateTime.UtcNow,
        };
    }
}