using AutomatedInvestment.Domain.Clients.Entities;
using AutomatedInvestment.Domain.Clients.ValueObjects;
using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutomatedInvestment.Infrastructure.Persistence.Configurations;

public class ClientConfiguration : IEntityTypeConfiguration<Client>
{
    public void Configure(EntityTypeBuilder<Client> builder)
    {
        // 1. Table Name
        builder.ToTable("Clients");

        // 2. Primary Key: UUID v7 stored as Binary(16)
        // This ensures MySQL 9 indexes the time-ordered GUIDs efficiently.
        builder.HasKey(x => x.Id);
        
        builder.Property(x => x.Id)
            .HasColumnType("binary(16)")
            .IsRequired();

        // 3. Name: Standard Varchar
        builder.Property(x => x.Name)
            .HasMaxLength(100)
            .IsRequired();

        // 4. Unique Business Keys (Email & CPF)
        // Standard approach: Unique Indexes
        builder.Property(c => c.Email)
            .HasConversion(
                e => e.Value,
                v => Email.Restore(v)) // Email.Restore apenas dá um 'new Email(v)'
            .HasColumnName("Email")
            .HasMaxLength(150);
            
        builder.HasIndex(x => x.Email)
            .IsUnique()
            .HasDatabaseName("IX_Clients_Email");

        builder.Property(c => c.Cpf)
            .HasConversion(
                cpf => cpf.Value,                         // Para o banco: extrai a string
                valorNoBanco => Cpf.Restore(valorNoBanco) // Para o C#: restaura o objeto
            )
            .HasColumnName("Cpf")
            .HasMaxLength(11) // CPF apenas números
            .IsRequired();

        builder.HasIndex(x => x.Cpf)
            .IsUnique()
            .HasDatabaseName("IX_Clients_Cpf");

        // 5. Booleans and Timestamps
        builder.Property(x => x.IsActive)
            .HasDefaultValue(true);

        builder.Property(x => x.CreatedAt)
            .HasColumnType("datetime(6)") // High precision for sorting
            .HasDefaultValueSql("CURRENT_TIMESTAMP(6)");
    }
}