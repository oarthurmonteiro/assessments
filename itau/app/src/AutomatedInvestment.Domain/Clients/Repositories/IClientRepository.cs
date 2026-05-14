using AutomatedInvestment.Domain.Clients.Entities;

namespace AutomatedInvestment.Domain.Repositories;

public interface IClientRepository
{
    Task<Client?> GetByIdAsync(Guid id);
    Task<bool> ExistsByEmailAsync(string email);
    Task AddAsync(Client client);
    Task UpdateAsync(Client client);
}