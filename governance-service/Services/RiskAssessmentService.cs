using GovernanceService.Data;
using GovernanceService.Models;

namespace GovernanceService.Services;

public class RiskAssessmentService
{
    private readonly GovernanceDbContext _context;
    private readonly ILogger<RiskAssessmentService> _logger;
    
    public RiskAssessmentService(GovernanceDbContext context, ILogger<RiskAssessmentService> logger)
    {
        _context = context;
        _logger = logger;
    }
    
    public async Task<RiskAssessment> AssessProjectRisk(AIProject project)
    {
        var riskDimensions = new List<RiskDimension>();
        
        // 1. Data Privacy & Security Assessment
        var privacyRisk = AssessDataPrivacyRisk(project);
        riskDimensions.Add(privacyRisk);
        
        // 2. Bias & Fairness Assessment
        var biasRisk = AssessBiasFairnessRisk(project);
        riskDimensions.Add(biasRisk);
        
        // 3. Transparency & Explainability Assessment
        var transparencyRisk = AssessTransparencyRisk(project);
        riskDimensions.Add(transparencyRisk);
        
        // 4. Regulatory Compliance Assessment
        var complianceRisk = AssessComplianceRisk(project);
        riskDimensions.Add(complianceRisk);
        
        // 5. Operational Risk Assessment
        var operationalRisk = AssessOperationalRisk(project);
        riskDimensions.Add(operationalRisk);
        
        // Calculate overall risk score (weighted average)
        var overallScore = riskDimensions.Average(d => d.Score);
        var riskLevel = overallScore < 4.0 ? "Low" : overallScore < 7.0 ? "Medium" : "High";
        
        // Determine compliance requirements
        var complianceRequirements = DetermineComplianceRequirements(project, riskDimensions);
        
        var assessment = new RiskAssessment
        {
            ProjectId = project.Id,
            OverallRiskScore = Math.Round(overallScore, 2),
            RiskLevel = riskLevel,
            RiskDimensions = riskDimensions,
            ComplianceRequirements = complianceRequirements,
            AssessmentDate = DateTime.UtcNow,
            AssessedBy = "System"
        };
        
        _logger.LogInformation($"Risk assessment completed for project {project.Name}: {riskLevel} ({overallScore:F2})");
        
        return assessment;
    }
    
    private RiskDimension AssessDataPrivacyRisk(AIProject project)
    {
        var score = 3.0; // Base score
        var recommendations = new List<string>();
        
        // Check for PII indicators
        var piiKeywords = new[] { "pii", "personal", "customer", "user data", "email", "phone", "address" };
        var hasPII = piiKeywords.Any(kw => 
            project.Description.Contains(kw, StringComparison.OrdinalIgnoreCase) ||
            project.DataSources.Any(ds => ds.Contains(kw, StringComparison.OrdinalIgnoreCase)));
        
        if (hasPII)
        {
            score += 4.0;
            recommendations.Add("Implement encryption at rest and in transit");
            recommendations.Add("Apply role-based access control (RBAC)");
            recommendations.Add("Conduct privacy impact assessment");
            recommendations.Add("Implement data minimization principles");
        }
        
        // Check for sensitive data
        var sensitiveKeywords = new[] { "health", "medical", "financial", "payment", "ssn", "credit card" };
        var hasSensitiveData = sensitiveKeywords.Any(kw => 
            project.Description.Contains(kw, StringComparison.OrdinalIgnoreCase));
        
        if (hasSensitiveData)
        {
            score += 2.0;
            recommendations.Add("Enhanced encryption requirements");
            recommendations.Add("Regular security audits");
        }
        
        score = Math.Min(10.0, score);
        var severity = score < 4.0 ? "Low" : score < 7.0 ? "Medium" : "High";
        
        return new RiskDimension
        {
            Name = "Data Privacy & Security",
            Score = score,
            Severity = severity,
            Explanation = hasPII 
                ? "Project handles PII and requires enhanced data protection measures"
                : "Standard data protection measures required",
            MitigationRecommendations = recommendations.Any() 
                ? recommendations 
                : new List<string> { "Implement standard security measures", "Regular security reviews" }
        };
    }
    
    private RiskDimension AssessBiasFairnessRisk(AIProject project)
    {
        var score = 5.0; // Medium baseline for AI projects
        var recommendations = new List<string>
        {
            "Test model across demographic groups",
            "Implement fairness metrics monitoring",
            "Regular bias audits",
            "Diverse training data validation"
        };
        
        // Higher risk for customer-facing applications
        if (project.Description.Contains("customer", StringComparison.OrdinalIgnoreCase) ||
            project.UseCase.Contains("customer", StringComparison.OrdinalIgnoreCase))
        {
            score += 2.0;
            recommendations.Add("Enhanced bias testing for customer-facing features");
        }
        
        var severity = score < 4.0 ? "Low" : score < 7.0 ? "Medium" : "High";
        
        return new RiskDimension
        {
            Name = "Bias & Fairness",
            Score = score,
            Severity = severity,
            Explanation = "AI models require bias testing and fairness evaluation",
            MitigationRecommendations = recommendations
        };
    }
    
    private RiskDimension AssessTransparencyRisk(AIProject project)
    {
        var score = 4.0;
        var recommendations = new List<string>
        {
            "Document model architecture and training data",
            "Implement model explainability features",
            "Maintain comprehensive documentation",
            "Provide decision explanations to users"
        };
        
        var severity = score < 4.0 ? "Low" : score < 7.0 ? "Medium" : "High";
        
        return new RiskDimension
        {
            Name = "Transparency & Explainability",
            Score = score,
            Severity = severity,
            Explanation = "Model interpretability and documentation requirements",
            MitigationRecommendations = recommendations
        };
    }
    
    private RiskDimension AssessComplianceRisk(AIProject project)
    {
        var score = 3.0;
        var recommendations = new List<string>();
        
        // Check for regulated industries
        var regulatedKeywords = new[] { "healthcare", "health", "medical", "financial", "banking", "insurance" };
        var isRegulated = regulatedKeywords.Any(kw => 
            project.Description.Contains(kw, StringComparison.OrdinalIgnoreCase) ||
            project.UseCase.Contains(kw, StringComparison.OrdinalIgnoreCase));
        
        if (isRegulated)
        {
            score += 4.0;
            recommendations.Add("Industry-specific compliance review required");
            recommendations.Add("Legal team consultation");
            recommendations.Add("Regulatory mapping and documentation");
        }
        
        recommendations.Add("Maintain audit trail");
        recommendations.Add("Regular compliance reviews");
        
        var severity = score < 4.0 ? "Low" : score < 7.0 ? "Medium" : "High";
        
        return new RiskDimension
        {
            Name = "Regulatory Compliance",
            Score = score,
            Severity = severity,
            Explanation = isRegulated 
                ? "Project operates in regulated industry requiring enhanced compliance"
                : "Standard compliance requirements apply",
            MitigationRecommendations = recommendations
        };
    }
    
    private RiskDimension AssessOperationalRisk(AIProject project)
    {
        var score = 4.0;
        var recommendations = new List<string>
        {
            "Implement monitoring and alerting",
            "Define error handling procedures",
            "Establish fallback mechanisms",
            "Regular performance testing"
        };
        
        var severity = score < 4.0 ? "Low" : score < 7.0 ? "Medium" : "High";
        
        return new RiskDimension
        {
            Name = "Operational Risk",
            Score = score,
            Severity = severity,
            Explanation = "System reliability and operational considerations",
            MitigationRecommendations = recommendations
        };
    }
    
    private List<string> DetermineComplianceRequirements(AIProject project, List<RiskDimension> riskDimensions)
    {
        var requirements = new List<string>();
        
        // Privacy compliance
        var privacyRisk = riskDimensions.FirstOrDefault(d => d.Name == "Data Privacy & Security");
        if (privacyRisk != null && privacyRisk.Score >= 7.0)
        {
            requirements.Add("GDPR compliance review");
            requirements.Add("CCPA compliance review");
            requirements.Add("Data Protection Officer approval");
        }
        
        // Regulatory compliance
        var complianceRisk = riskDimensions.FirstOrDefault(d => d.Name == "Regulatory Compliance");
        if (complianceRisk != null && complianceRisk.Score >= 7.0)
        {
            requirements.Add("Industry-specific regulatory compliance");
            requirements.Add("Legal team review");
        }
        
        // General requirements
        requirements.Add("AI Ethics Board review");
        requirements.Add("Security assessment");
        
        return requirements.Distinct().ToList();
    }
}
