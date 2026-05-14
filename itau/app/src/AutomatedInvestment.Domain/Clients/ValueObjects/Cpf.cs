namespace AutomatedInvestment.Domain.Clients.ValueObjects;

public record Cpf
{
    public string Value { get; init; }

    private Cpf(string value) => Value = value;

    public static Result<Cpf> Create(string value)
    {
        if (string.IsNullOrWhiteSpace(value))
            return Result<Cpf>.Failure("CPF é obrigatório.");

        var cleanedCpf = Clean(value);

        if (cleanedCpf.Length != 11)
            return Result<Cpf>.Failure("CPF deve conter 11 dígitos.");

        if (HasAllSameDigits(cleanedCpf))
            return Result<Cpf>.Failure("CPF inválido (dígitos repetidos).");

        if (!IsValid(cleanedCpf))
            return Result<Cpf>.Failure($"O CPF '{value}' é inválido.");

        return new Cpf(cleanedCpf);
    }

    // Método para o EF Core (sem validação)
    public static Cpf Restore(string value) => new(value);

    private static string Clean(string value) 
        => new(value.Where(char.IsDigit).ToArray());

    private static bool HasAllSameDigits(string cpf) 
        => cpf.All(c => c == cpf[0]);

    private static bool IsValid(string cpf)
    {
        // Algoritmo oficial de validação de CPF
        int[] multiplier1 = [10, 9, 8, 7, 6, 5, 4, 3, 2];
        int[] multiplier2 = [11, 10, 9, 8, 7, 6, 5, 4, 3, 2];

        string tempCpf = cpf[..9];
        int sum = 0;

        for (int i = 0; i < 9; i++)
            sum += (tempCpf[i] - '0') * multiplier1[i];

        int remainder = sum % 11;
        remainder = remainder < 2 ? 0 : 11 - remainder;

        string digit = remainder.ToString();
        tempCpf += digit;
        sum = 0;

        for (int i = 0; i < 10; i++)
            sum += (tempCpf[i] - '0') * multiplier2[i];

        remainder = sum % 11;
        remainder = remainder < 2 ? 0 : 11 - remainder;

        digit += remainder.ToString();

        return cpf.EndsWith(digit);
    }
    
    public static implicit operator string(Cpf cpf) => cpf.Value;
    public override string ToString() => Value;
}