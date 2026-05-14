using AutomatedInvestment.Domain.Products.ValueObjects;

namespace AutomatedInvestment.Domain.Tests.Products.ValueObjects;

public class BasketAssetTests
{
    [Fact]
    public void Create_WithValidAssetPercentage_ShouldReturnSuccess()
    {
        var validProduct = Guid.CreateVersion7();
        var validPercentage = 50.00m;

        var result = BasketAsset.Create(validProduct, validPercentage);

        Assert.True(result.IsSuccess);
        Assert.Equal(validProduct, result.Value.ProductId);
        Assert.Equal(validPercentage, result.Value.Percentage);
    }

    [Fact]
    public void Create_WithEmptyGuid_ShouldReturnFailure()
    {
        var emptyGuid = Guid.Empty;

        var result = BasketAsset.Create(emptyGuid, 50m);

        Assert.True(result.IsFailure);
        Assert.Equal("ID do produto não pode ser nulo.", result.Errors.First());
    }

    [Theory]
    [InlineData(0)]
    [InlineData(-10)]
    [InlineData(100.01)]
    public void Create_WithInvalidPercentage_ShouldReturnFailure(decimal invalidPercentage)
    {
        var result = BasketAsset.Create(Guid.NewGuid(), invalidPercentage);

        Assert.True(result.IsFailure);
        Assert.Equal("A porcentagem deve estar entre 0.01 e 100.", result.Errors.First());
    }
}