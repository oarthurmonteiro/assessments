using AutomatedInvestment.Domain.Products.Entities;
using AutomatedInvestment.Domain.Products.ValueObjects;

namespace AutomatedInvestment.Domain.Tests.Products.Entities;

public class BasketTests
{
    [Fact]
    public void Create_WithValidData_ShouldReturnSuccess()
    {
        var name = "Top Five Março";
        var items = new List<BasketAsset>
        {
            BasketAsset.Create(Guid.NewGuid(), 60m).Value,
            BasketAsset.Create(Guid.NewGuid(), 40m).Value
        };

        var result = Basket.Create(name, items);

        Assert.True(result.IsSuccess);
        Assert.Equal(name, result.Value.Name);
        Assert.Equal(2, result.Value.Items.Count);
        Assert.True(result.Value.IsActive);
    }

    [Theory]
    [InlineData(40, 50)] // Soma 90 (Inválido)
    [InlineData(60, 50)] // Soma 110 (Inválido)
    public void Create_WhenPercentageSumIsNot100_ShouldReturnFailure(decimal p1, decimal p2)
    {
        // Arrange: Criamos itens que individualmente são VÁLIDOS (entre 0 e 100)
        var items = new List<BasketAsset> 
        { 
            BasketAsset.Create(Guid.NewGuid(), p1).Value, 
            BasketAsset.Create(Guid.NewGuid(), p2).Value 
        };

        // Act: A falha deve acontecer aqui, na regra da Cesta
        var result = Basket.Create("Cesta Inválida", items);

        // Assert
        Assert.True(result.IsFailure);
        Assert.Contains("A soma das porcentagens deve ser 100%", result.Errors.First());
    }

    [Fact]
    public void Create_WhenItemsListIsEmpty_ShouldReturnFailure()
    {
        // Act
        var result = Basket.Create("Cesta Vazia", new List<BasketAsset>());

        // Assert
        Assert.True(result.IsFailure);
        Assert.Equal("A cesta deve conter ao menos um ativo.", result.Errors.First());
    }
}