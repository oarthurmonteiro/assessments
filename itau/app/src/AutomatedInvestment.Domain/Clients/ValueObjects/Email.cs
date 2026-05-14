namespace AutomatedInvestment.Domain.Clients.ValueObjects;

public record Email
{
    public string Value { get; init; }

    private Email(string value) => Value = value;

    public static Result<Email> Create(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return Result<Email>.Failure("O e-mail não pode estar vazio.");

        var trimmedEmail = value.Trim().ToLower();

        if (!IsValid(trimmedEmail))
            return Result<Email>.Failure($"O formato do e-mail '{value}' é inválido.");

        return Result<Email>.Success(new Email(trimmedEmail));
    }

    private static bool IsValid(string email)
    {
        try
        {
            var addr = new System.Net.Mail.MailAddress(email);
            return addr.Address == email;
        }
        catch
        {
            return false;
        }
    }


    public static Email Restore(string value) => new(value);
    
    // Opcional: Conversão implícita para facilitar o uso
    public static implicit operator string(Email email) => email.Value;
    public override string ToString() => Value;
}