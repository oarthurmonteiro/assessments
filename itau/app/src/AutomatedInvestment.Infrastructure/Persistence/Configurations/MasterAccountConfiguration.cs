using AutomatedInvestment.Domain.Accounts.Entities;

using Microsoft.EntityFrameworkCore;
using Microsoft.EntityFrameworkCore.Metadata.Builders;

namespace AutomatedInvestment.Infrastructure.Persistence.Configurations;

public class MasterAccountConfiguration : IEntityTypeConfiguration<MasterAccount>
{
    public void Configure(EntityTypeBuilder<MasterAccount> builder)
    {
        builder.ToTable("MasterAccounts");

        builder.Property(m => m.InternalCode)
               .HasMaxLength(50)
               .IsRequired();
    }
}