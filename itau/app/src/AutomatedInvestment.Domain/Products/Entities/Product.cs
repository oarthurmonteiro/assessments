namespace AutomatedInvestment.Domain.Products.Entities;

public class Product : BaseEntity
{
    public string Ticker { get; private set; } = null!; // Ex: PETR4, ITUB4
    public string Name { get; private set; } = null!;
    public decimal MinimumInvestment { get; private set; }
    public bool IsActive { get; private set; }

    private Product() { } // EF Core

    public static Result<Product> Create(string ticker, string name, decimal minInvestment)
    {
        if (string.IsNullOrWhiteSpace(ticker))
            return Result<Product>.Failure("Ticker é obrigatório.");
            
        if (minInvestment < 0)
            return Result<Product>.Failure("Investimento mínimo não pode ser negativo.");

        return new Product
        {
            Id = Guid.CreateVersion7(),
            Ticker = ticker.ToUpper().Trim(),
            Name = name,
            MinimumInvestment = minInvestment,
            IsActive = true
        };
    }
}