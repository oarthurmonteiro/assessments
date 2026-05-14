namespace AutomatedInvestment.Domain.Products.ValueObjects;

public sealed record BasketAsset
{
    public Guid ProductId { get; init; }
    public decimal Percentage { get; init; }

    private BasketAsset() {}

    public static Result<BasketAsset> Create(Guid productId, decimal percentage)
    {
        if (productId == Guid.Empty)
            return Result<BasketAsset>.Failure("ID do produto não pode ser nulo.");

        if (percentage <= 0 || percentage > 100)
            return Result<BasketAsset>.Failure("A porcentagem deve estar entre 0.01 e 100.");

        return new BasketAsset { ProductId = productId, Percentage = percentage };
    }
}