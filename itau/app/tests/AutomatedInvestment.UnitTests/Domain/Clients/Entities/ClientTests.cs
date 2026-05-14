using AutomatedInvestment.Domain.Clients.Entities;
using AutomatedInvestment.Domain.Clients.ValueObjects;

namespace AutomatedInvestment.Domain.Tests.Clients.Entities;

public class ClientTests
{
    [Fact]
    public void Create_WithValidData_ShouldReturnSuccess()
    {
        var name = "Arthur Monteiro";
        var email = "arthur@teste.com";
        var cpf = "12345678909";

        var result = Client.Create(name, email, cpf);

        Assert.True(result.IsSuccess);
        Assert.NotNull(result.Value);
        Assert.Equal(name, result.Value.Name);
        Assert.Equal(cpf, result.Value.Cpf.Value);
    }

    [Fact]
    public void Create_WithInvalidName_ShouldReturnFailure()
    {
        var invalidName = ""; 
        var email = "arthur@teste.com";
        var cpf = "12345678909";

        var result = Client.Create(invalidName, email, cpf);

        Assert.True(result.IsFailure);
        Assert.Contains("Nome é obrigatório.", result.Errors);
    }

    [Fact]
    public void Create_WithInvalidCpfAndEmail_ShouldAccumulateAllErrors()
    {
        var name = "Arthur";
        var invalidEmail = "email-errado";
        var invalidCpf = "123";

        var result = Client.Create(name, invalidEmail, invalidCpf);

        Assert.True(result.IsFailure);
        Assert.True(result.Errors.Count == 2); 
    }
}