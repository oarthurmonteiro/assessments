using Microsoft.EntityFrameworkCore;
using AutomatedInvestment.Domain.Clients.Entities;
using AutomatedInvestment.Domain.Accounts.Entities;

namespace AutomatedInvestment.Infrastructure.Persistence;

public class AppDbContext(DbContextOptions<AppDbContext> options) : DbContext(options)
{
    // DbSets: Note que você pode ter o DbSet da base e das filhas
    public DbSet<Client> Clients { get; set; }
    // public DbSet<Account> Accounts { get; set; }
    // public DbSet<ClientAccount> ClientAccounts { get; set; }
    // public DbSet<MasterAccount> MasterAccounts { get; set; }
    

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
                // Always call the base first to ensure internal EF logic runs
        base.OnModelCreating(modelBuilder);

        // Scans the assembly for all IEntityTypeConfiguration classes
        modelBuilder.ApplyConfigurationsFromAssembly(typeof(AppDbContext).Assembly);
    }
}
