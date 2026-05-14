using AutomatedInvestment.Domain.Accounts.Entities;

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutomatedInvestment.Infrastructure.Persistence.Configurations;

public class AccountConfiguration : IEntityTypeConfiguration<Account>
{
    public void Configure(EntityTypeBuilder<Account> builder)
    {
        
        builder.ToTable("Accounts");

        // 2. Primary Key: UUID v7 stored as Binary(16)
        // This ensures MySQL 9 indexes the time-ordered GUIDs efficiently.
        builder.HasKey(x => x.Id);
        
        builder.Property(x => x.Id)
            .HasColumnType("binary(16)")
            .IsRequired();

        builder.Property(a => a.AccountNumber)
            .HasMaxLength(20)
            .IsRequired();

        builder.Property(a => a.Type)
            .HasConversion<int>() // Ou .HasConversion<string>() se preferir o nome
            .IsRequired();

        // Configura o TPT (Table-per-Type)
        // O EF usará a coluna "Type" para saber qual tabela filha consultar
        // builder.HasDiscriminator(a => a.Type)
        //        .HasValue<ClientAccount>(AccountType.Child)
        //        .HasValue<MasterAccount>(AccountType.Master);

        builder.Property(x => x.CreatedAt)
            .HasColumnType("datetime(6)") // High precision for sorting
            .HasDefaultValueSql("CURRENT_TIMESTAMP(6)");
    }
}