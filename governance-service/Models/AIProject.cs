using System.ComponentModel.DataAnnotations;
using System.ComponentModel.DataAnnotations.Schema;

namespace GovernanceService.Models;

public class AIProject
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    
    [Required]
    [MaxLength(200)]
    public string Name { get; set; } = string.Empty;
    
    [Required]
    public string Description { get; set; } = string.Empty;
    
    [Required]
    [MaxLength(100)]
    public string UseCase { get; set; } = string.Empty;
    
    public List<string> DataSources { get; set; } = new();
    
    public List<string> Stakeholders { get; set; } = new();
    
    [Required]
    [MaxLength(50)]
    public string Status { get; set; } = "Pending"; // Pending, Approved, Rejected, InDevelopment, Production, Retired
    
    [Range(0, 10)]
    public double RiskScore { get; set; }
    
    [MaxLength(20)]
    public string RiskLevel { get; set; } = "Unknown"; // Low, Medium, High
    
    public bool ApprovalRequired { get; set; }
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
    
    [MaxLength(100)]
    public string? CreatedBy { get; set; }
    
    // Navigation properties
    public virtual ICollection<RiskAssessment> RiskAssessments { get; set; } = new List<RiskAssessment>();
    public virtual ICollection<ComplianceCheck> ComplianceChecks { get; set; } = new List<ComplianceCheck>();
}

public class RiskAssessment
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    
    [Required]
    public Guid ProjectId { get; set; }
    
    [ForeignKey("ProjectId")]
    public virtual AIProject? Project { get; set; }
    
    [Range(0, 10)]
    public double OverallRiskScore { get; set; }
    
    [MaxLength(20)]
    public string RiskLevel { get; set; } = "Unknown";
    
    public List<RiskDimension> RiskDimensions { get; set; } = new();
    
    public List<string> ComplianceRequirements { get; set; } = new();
    
    public DateTime AssessmentDate { get; set; } = DateTime.UtcNow;
    
    [MaxLength(100)]
    public string? AssessedBy { get; set; }
}

public class RiskDimension
{
    public string Name { get; set; } = string.Empty;
    
    [Range(0, 10)]
    public double Score { get; set; }
    
    public string Severity { get; set; } = "Unknown"; // Low, Medium, High
    
    public string Explanation { get; set; } = string.Empty;
    
    public List<string> MitigationRecommendations { get; set; } = new();
}

public class ComplianceCheck
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    
    [Required]
    public Guid ProjectId { get; set; }
    
    [ForeignKey("ProjectId")]
    public virtual AIProject? Project { get; set; }
    
    [Required]
    [MaxLength(100)]
    public string PolicyName { get; set; } = string.Empty;
    
    [Required]
    [MaxLength(50)]
    public string PolicyArea { get; set; } = string.Empty; // DataPrivacy, BiasFairness, Security, etc.
    
    public bool IsCompliant { get; set; }
    
    public string? NonComplianceReason { get; set; }
    
    public List<string> RequiredActions { get; set; } = new();
    
    public DateTime CheckedAt { get; set; } = DateTime.UtcNow;
    
    [MaxLength(100)]
    public string? CheckedBy { get; set; }
}

public class CompliancePolicy
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    
    [Required]
    [MaxLength(100)]
    public string Name { get; set; } = string.Empty;
    
    [Required]
    [MaxLength(50)]
    public string Area { get; set; } = string.Empty;
    
    [Required]
    public string Description { get; set; } = string.Empty;
    
    public List<string> Requirements { get; set; } = new();
    
    public bool ApprovalRequired { get; set; }
    
    public bool IsActive { get; set; } = true;
    
    public DateTime CreatedAt { get; set; } = DateTime.UtcNow;
    
    public DateTime UpdatedAt { get; set; } = DateTime.UtcNow;
}

public class AuditLog
{
    [Key]
    public Guid Id { get; set; } = Guid.NewGuid();
    
    [Required]
    [MaxLength(50)]
    public string EntityType { get; set; } = string.Empty; // AIProject, RiskAssessment, etc.
    
    [Required]
    public Guid EntityId { get; set; }
    
    [Required]
    [MaxLength(50)]
    public string Action { get; set; } = string.Empty; // Created, Updated, Deleted, Approved, etc.
    
    public string? Details { get; set; }
    
    [MaxLength(100)]
    public string? PerformedBy { get; set; }
    
    public DateTime Timestamp { get; set; } = DateTime.UtcNow;
    
    public Dictionary<string, object> Metadata { get; set; } = new();
}
