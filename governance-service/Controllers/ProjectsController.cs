using Microsoft.AspNetCore.Mvc;
using Microsoft.EntityFrameworkCore;
using GovernanceService.Data;
using GovernanceService.Models;
using GovernanceService.Services;

namespace GovernanceService.Controllers;

[ApiController]
[Route("api/[controller]")]
public class ProjectsController : ControllerBase
{
    private readonly GovernanceDbContext _context;
    private readonly RiskAssessmentService _riskService;
    private readonly AuditService _auditService;
    private readonly ILogger<ProjectsController> _logger;
    
    public ProjectsController(
        GovernanceDbContext context,
        RiskAssessmentService riskService,
        AuditService auditService,
        ILogger<ProjectsController> logger)
    {
        _context = context;
        _riskService = riskService;
        _auditService = auditService;
        _logger = logger;
    }
    
    [HttpGet]
    public async Task<ActionResult<IEnumerable<AIProject>>> GetProjects(
        [FromQuery] string? status = null,
        [FromQuery] string? riskLevel = null)
    {
        var query = _context.AIProjects
            .Include(p => p.RiskAssessments)
            .Include(p => p.ComplianceChecks)
            .AsQueryable();
        
        if (!string.IsNullOrEmpty(status))
        {
            query = query.Where(p => p.Status == status);
        }
        
        if (!string.IsNullOrEmpty(riskLevel))
        {
            query = query.Where(p => p.RiskLevel == riskLevel);
        }
        
        var projects = await query.OrderByDescending(p => p.CreatedAt).ToListAsync();
        return Ok(projects);
    }
    
    [HttpGet("{id}")]
    public async Task<ActionResult<AIProject>> GetProject(Guid id)
    {
        var project = await _context.AIProjects
            .Include(p => p.RiskAssessments)
            .Include(p => p.ComplianceChecks)
            .FirstOrDefaultAsync(p => p.Id == id);
        
        if (project == null)
        {
            return NotFound();
        }
        
        return Ok(project);
    }
    
    [HttpPost]
    public async Task<ActionResult<AIProject>> CreateProject(AIProject project)
    {
        project.Id = Guid.NewGuid();
        project.CreatedAt = DateTime.UtcNow;
        project.UpdatedAt = DateTime.UtcNow;
        project.Status = "Pending";
        
        // Perform risk assessment
        var riskAssessment = await _riskService.AssessProjectRisk(project);
        project.RiskScore = riskAssessment.OverallRiskScore;
        project.RiskLevel = riskAssessment.RiskLevel;
        project.ApprovalRequired = riskAssessment.OverallRiskScore >= 4.0;
        
        _context.AIProjects.Add(project);
        
        // Add risk assessment
        riskAssessment.ProjectId = project.Id;
        _context.RiskAssessments.Add(riskAssessment);
        
        await _context.SaveChangesAsync();
        
        // Log audit trail
        await _auditService.LogAction("AIProject", project.Id, "Created", 
            $"Project '{project.Name}' created with risk level {project.RiskLevel}");
        
        _logger.LogInformation($"Created project {project.Id} - {project.Name}");
        
        return CreatedAtAction(nameof(GetProject), new { id = project.Id }, project);
    }
    
    [HttpPut("{id}")]
    public async Task<IActionResult> UpdateProject(Guid id, AIProject project)
    {
        if (id != project.Id)
        {
            return BadRequest();
        }
        
        var existingProject = await _context.AIProjects.FindAsync(id);
        if (existingProject == null)
        {
            return NotFound();
        }
        
        existingProject.Name = project.Name;
        existingProject.Description = project.Description;
        existingProject.UseCase = project.UseCase;
        existingProject.DataSources = project.DataSources;
        existingProject.Stakeholders = project.Stakeholders;
        existingProject.Status = project.Status;
        existingProject.UpdatedAt = DateTime.UtcNow;
        
        await _context.SaveChangesAsync();
        
        await _auditService.LogAction("AIProject", id, "Updated", 
            $"Project '{project.Name}' updated");
        
        return NoContent();
    }
    
    [HttpDelete("{id}")]
    public async Task<IActionResult> DeleteProject(Guid id)
    {
        var project = await _context.AIProjects.FindAsync(id);
        if (project == null)
        {
            return NotFound();
        }
        
        _context.AIProjects.Remove(project);
        await _context.SaveChangesAsync();
        
        await _auditService.LogAction("AIProject", id, "Deleted", 
            $"Project '{project.Name}' deleted");
        
        return NoContent();
    }
    
    [HttpPost("{id}/approve")]
    public async Task<IActionResult> ApproveProject(Guid id)
    {
        var project = await _context.AIProjects.FindAsync(id);
        if (project == null)
        {
            return NotFound();
        }
        
        project.Status = "Approved";
        project.UpdatedAt = DateTime.UtcNow;
        
        await _context.SaveChangesAsync();
        
        await _auditService.LogAction("AIProject", id, "Approved", 
            $"Project '{project.Name}' approved");
        
        return Ok(project);
    }
    
    [HttpGet("metrics")]
    public async Task<ActionResult<object>> GetMetrics()
    {
        var totalProjects = await _context.AIProjects.CountAsync();
        var activeProjects = await _context.AIProjects.CountAsync(p => p.Status == "InDevelopment" || p.Status == "Production");
        var pendingApproval = await _context.AIProjects.CountAsync(p => p.Status == "Pending");
        
        var riskDistribution = await _context.AIProjects
            .GroupBy(p => p.RiskLevel)
            .Select(g => new { RiskLevel = g.Key, Count = g.Count() })
            .ToListAsync();
        
        return Ok(new
        {
            TotalProjects = totalProjects,
            ActiveProjects = activeProjects,
            PendingApproval = pendingApproval,
            RiskDistribution = riskDistribution
        });
    }
}
