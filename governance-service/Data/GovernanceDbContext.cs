using Microsoft.EntityFrameworkCore;
using GovernanceService.Models;

namespace GovernanceService.Data;

public class GovernanceDbContext : DbContext
{
    public GovernanceDbContext(DbContextOptions<GovernanceDbContext> options)
        : base(options)
    {
    }
    
    public DbSet<AIProject> AIProjects { get; set; }
    public DbSet<RiskAssessment> RiskAssessments { get; set; }
    public DbSet<ComplianceCheck> ComplianceChecks { get; set; }
    public DbSet<CompliancePolicy> CompliancePolicies { get; set; }
    public DbSet<AuditLog> AuditLogs { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        base.OnModelCreating(modelBuilder);
        
        // AIProject configuration
        modelBuilder.Entity<AIProject>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Name);
            entity.HasIndex(e => e.Status);
            entity.HasIndex(e => e.RiskLevel);
            
            entity.Property(e => e.DataSources)
                .HasConversion(
                    v => string.Join(',', v),
                    v => v.Split(',', StringSplitOptions.RemoveEmptyEntries).ToList()
                );
            
            entity.Property(e => e.Stakeholders)
                .HasConversion(
                    v => string.Join(',', v),
                    v => v.Split(',', StringSplitOptions.RemoveEmptyEntries).ToList()
                );
        });
        
        // RiskAssessment configuration
        modelBuilder.Entity<RiskAssessment>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.ProjectId);
            entity.HasIndex(e => e.AssessmentDate);
            
            entity.Property(e => e.RiskDimensions)
                .HasConversion(
                    v => System.Text.Json.JsonSerializer.Serialize(v, (System.Text.Json.JsonSerializerOptions?)null),
                    v => System.Text.Json.JsonSerializer.Deserialize<List<RiskDimension>>(v, (System.Text.Json.JsonSerializerOptions?)null) ?? new List<RiskDimension>()
                );
            
            entity.Property(e => e.ComplianceRequirements)
                .HasConversion(
                    v => string.Join(',', v),
                    v => v.Split(',', StringSplitOptions.RemoveEmptyEntries).ToList()
                );
            
            entity.HasOne(e => e.Project)
                .WithMany(p => p.RiskAssessments)
                .HasForeignKey(e => e.ProjectId)
                .OnDelete(DeleteBehavior.Cascade);
        });
        
        // ComplianceCheck configuration
        modelBuilder.Entity<ComplianceCheck>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.ProjectId);
            entity.HasIndex(e => e.PolicyArea);
            entity.HasIndex(e => e.IsCompliant);
            
            entity.Property(e => e.RequiredActions)
                .HasConversion(
                    v => string.Join(',', v),
                    v => v.Split(',', StringSplitOptions.RemoveEmptyEntries).ToList()
                );
            
            entity.HasOne(e => e.Project)
                .WithMany(p => p.ComplianceChecks)
                .HasForeignKey(e => e.ProjectId)
                .OnDelete(DeleteBehavior.Cascade);
        });
        
        // CompliancePolicy configuration
        modelBuilder.Entity<CompliancePolicy>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Name).IsUnique();
            entity.HasIndex(e => e.Area);
            entity.HasIndex(e => e.IsActive);
            
            entity.Property(e => e.Requirements)
                .HasConversion(
                    v => string.Join(',', v),
                    v => v.Split(',', StringSplitOptions.RemoveEmptyEntries).ToList()
                );
        });
        
        // AuditLog configuration
        modelBuilder.Entity<AuditLog>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.EntityType);
            entity.HasIndex(e => e.EntityId);
            entity.HasIndex(e => e.Timestamp);
            
            entity.Property(e => e.Metadata)
                .HasConversion(
                    v => System.Text.Json.JsonSerializer.Serialize(v, (System.Text.Json.JsonSerializerOptions?)null),
                    v => System.Text.Json.JsonSerializer.Deserialize<Dictionary<string, object>>(v, (System.Text.Json.JsonSerializerOptions?)null) ?? new Dictionary<string, object>()
                );
        });
        
        // Seed initial compliance policies
        SeedCompliancePolicies(modelBuilder);
    }
    
    private void SeedCompliancePolicies(ModelBuilder modelBuilder)
    {
        var policies = new[]
        {
            new CompliancePolicy
            {
                Id = Guid.NewGuid(),
                Name = "Data Privacy Policy",
                Area = "DataPrivacy",
                Description = "All AI projects must comply with data privacy regulations including GDPR and CCPA",
                Requirements = new List<string>
                {
                    "Data minimization",
                    "Encryption at rest and in transit",
                    "Role-based access control",
                    "Privacy impact assessment for PII"
                },
                ApprovalRequired = true,
                IsActive = true
            },
            new CompliancePolicy
            {
                Id = Guid.NewGuid(),
                Name = "Bias and Fairness Policy",
                Area = "BiasFairness",
                Description = "AI systems must be tested for bias and ensure fair outcomes",
                Requirements = new List<string>
                {
                    "Diverse training data",
                    "Bias testing across demographics",
                    "Fairness metrics monitoring",
                    "Regular bias audits"
                },
                ApprovalRequired = false,
                IsActive = true
            },
            new CompliancePolicy
            {
                Id = Guid.NewGuid(),
                Name = "Security Policy",
                Area = "Security",
                Description = "Implement robust security measures for AI systems",
                Requirements = new List<string>
                {
                    "Secure API endpoints",
                    "Input validation",
                    "Output sanitization",
                    "Security testing"
                },
                ApprovalRequired = false,
                IsActive = true
            }
        };
        
        modelBuilder.Entity<CompliancePolicy>().HasData(policies);
    }
}
