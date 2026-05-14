namespace AutomatedInvestment.Domain.Accounts.Entities;

public enum AccountType
{
    Master = 1,
    Child = 2
}

public abstract class Account : BaseEntity
{
    public string AccountNumber { get; protected set; } = null!;
    public AccountType Type { get; protected set; }

    // private readonly List<Position> _positions = new();
    // public IReadOnlyCollection<Position> Positions => _positions.AsReadOnly();

    // public void CreditAsset(Guid productId, int quantity, decimal unitPrice)
    // {
    //     if (quantity <= 0) throw new DomainException("Quantidade deve ser positiva.");

    //     var position = _positions.FirstOrDefault(x => x.ProductId == productId);

    //     if (position == null)
    //     {
    //         // RN-042: Primeira compra define o preço médio inicial
    //         _positions.Add(new Position(Id, productId, quantity, unitPrice));
    //     }
    //     else
    //     {
    //         // RN-042: Recalcula preço médio se for uma conta de cliente
    //         // Na Master, o preço médio pode ser apenas informativo ou zero
    //         position.UpdateAveragePrice(quantity, unitPrice);
    //     }
    // }

    // public void DebitAsset(Guid productId, int quantity)
    // {
    //     var position = _positions.FirstOrDefault(x => x.ProductId == productId);
        
    //     if (position == null || position.Quantity < quantity)
    //         throw new DomainException("Saldo insuficiente na custódia.");

    //     // RN-043: Venda/Débito NÃO altera o preço médio
    //     position.DecreaseQuantity(quantity);

    //     if (position.Quantity == 0)
    //         _positions.Remove(position);
    // }
}