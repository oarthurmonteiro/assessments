using AutomatedInvestment.Domain.Clients.ValueObjects;

namespace AutomatedInvestment.Domain.Tests.Clients.ValueObjects;

public class CpfTests
{
    [Fact] // Indica um teste que sempre deve ser verdadeiro
    public void Create_WithValidCpf_ShouldReturnSuccess()
    {
        var validCpf = "12345678909";

        var result = Cpf.Create(validCpf);

        Assert.True(result.IsSuccess);
        Assert.Equal(validCpf, result.Value);
    }

    [Theory] // Indica um teste que roda várias vezes com dados diferentes
    [InlineData("123")]
    [InlineData("11111111111")]
    [InlineData("abc12345678")]
    public void Create_WithInvalidCpf_ShouldReturnFailure(string invalidCpf)
    {
        // Act
        var result = Cpf.Create(invalidCpf);

        // Assert
        Assert.True(result.IsFailure);
        Assert.NotEmpty(result.Errors);
    }
}