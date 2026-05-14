using AutomatedInvestment.Domain.Accounts.Entities;

namespace AutomatedInvestment.Domain.Repositories;

public interface IAccountRepository
{
    Task<Account?> GetByIdAsync(Guid id);
    Task AddAsync(Account account);
}