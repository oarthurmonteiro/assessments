using AutomatedInvestment.Domain.Accounts.Entities;

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutomatedInvestment.Infrastructure.Persistence.Configurations;

public class ClientAccountConfiguration : IEntityTypeConfiguration<ClientAccount>
{
    public void Configure(EntityTypeBuilder<ClientAccount> builder)
    {
        // Ao dar um ToTable diferente, o EF entende que é TPT (tabelas separadas)
        builder.ToTable("ClientAccounts"); 

        builder.Property(c => c.ClientId)
               .IsRequired();

        builder.Property(c => c.Status)
               .HasConversion<int>() // Salva o Enum como Int no banco
               .IsRequired();

        // Nota: Você não configura o "Id" aqui. 
        // O EF automaticamente mapeia o Id herdado como PK e FK para "accounts".
    }
}