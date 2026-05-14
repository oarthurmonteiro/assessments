using AutomatedInvestment.Domain.Products.ValueObjects;

namespace AutomatedInvestment.Domain.Products.Entities;

public class Basket : BaseEntity
{
    public string Name { get; private set; } = null!;
    public bool IsActive { get; private set; }
    public DateTime? DeactivatedAt { get; private set; }

    private readonly List<BasketAsset> _items = new();
    public IReadOnlyCollection<BasketAsset> Items => _items.AsReadOnly();

    private Basket() { } 

    public static Result<Basket> Create(string name, List<BasketAsset> items)
    {
        if (string.IsNullOrWhiteSpace(name))
            return Result<Basket>.Failure("Nome da cesta é obrigatório.");

        if (items == null || !items.Any())
            return Result<Basket>.Failure("A cesta deve conter ao menos um ativo.");

        // Regra crucial para o investimento automatizado
        var totalPercentage = items.Sum(x => x.Percentage);
        if (totalPercentage != 100)
            return Result<Basket>.Failure($"A soma das porcentagens deve ser 100%. Atual: {totalPercentage}%");

        var basket = new Basket
        {
            Id = Guid.CreateVersion7(),
            Name = name,
            IsActive = true
        };
        
        basket._items.AddRange(items);
        return basket;
    }

    public void Deactivate()
    {
        IsActive = false;
        DeactivatedAt = DateTime.UtcNow;
    }
}