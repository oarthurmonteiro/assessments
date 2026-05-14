using AutomatedInvestment.Domain.Clients.ValueObjects;

namespace AutomatedInvestment.Domain.Tests.Clients.ValueObjects;

public class EmailTests
{
    [Fact] // Indica um teste que sempre deve ser verdadeiro
    public void Create_WithValidEmail_ShouldReturnSuccess()
    {
        var validEmail = "email@test.com";

        var result = Email.Create(validEmail);

        Assert.True(result.IsSuccess);
        Assert.Equal(validEmail, result.Value);
    }

    [Theory] // Indica um teste que roda várias vezes com dados diferentes
    [InlineData("email")]
    [InlineData("@test")]
    [InlineData("e@")]
    public void Create_WithInvalidEmail_ShouldReturnFailure(string invalidEmail)
    {
        // Act
        var result = Email.Create(invalidEmail);

        // Assert
        Assert.True(result.IsFailure);
        Assert.NotEmpty(result.Errors);
    }
}