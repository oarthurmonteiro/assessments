using AutomatedInvestment.Domain.Clients.ValueObjects;

namespace AutomatedInvestment.Domain.Clients.Entities;

public class Client : BaseEntity
{
    public string Name { get; private set; } = null!;
    public Email Email { get; private set; } = null!;
    public Cpf Cpf { get; private set; } = null!;
    public bool IsActive { get; private set; }

    // 1. CONSTRUTOR PRIVADO: Protege a integridade
    // O EF Core usará este para "hidratar" o objeto do banco
    private Client() { } 

    private Client(string name, Email email, Cpf cpf)
    {
        Id = Guid.CreateVersion7();
        Name = name;
        Email = email;
        Cpf = cpf;
        IsActive = true;
        CreatedAt = DateTime.UtcNow;
    }

    // 2. FACTORY METHOD: O único jeito de criar um cliente novo no sistema
    public static Result<Client> Create(string name, string emailRaw, string cpfRaw)
    {
        var emailResult = Email.Create(emailRaw);
        var cpfResult = Cpf.Create(cpfRaw);

        var reasons = new List<string>();
        if (emailResult.IsFailure) reasons.AddRange(emailResult.Errors);
        if (cpfResult.IsFailure) reasons.AddRange(cpfResult.Errors);
        
        if (string.IsNullOrWhiteSpace(name)) 
            reasons.Add("Nome é obrigatório.");

        if (reasons is not [])
            return Result<Client>.Failure(reasons);

        return Result<Client>.Success(new Client(name, emailResult.Value, cpfResult.Value));
    }

    public void Deactivate() => IsActive = false;
}