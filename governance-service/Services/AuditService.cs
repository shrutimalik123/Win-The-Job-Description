using GovernanceService.Data;
using GovernanceService.Models;

namespace GovernanceService.Services;

public class AuditService
{
    private readonly GovernanceDbContext _context;
    private readonly ILogger<AuditService> _logger;
    
    public AuditService(GovernanceDbContext context, ILogger<AuditService> logger)
    {
        _context = context;
        _logger = logger;
    }
    
    public async Task LogAction(
        string entityType,
        Guid entityId,
        string action,
        string? details = null,
        string? performedBy = null,
        Dictionary<string, object>? metadata = null)
    {
        var auditLog = new AuditLog
        {
            EntityType = entityType,
            EntityId = entityId,
            Action = action,
            Details = details,
            PerformedBy = performedBy ?? "System",
            Timestamp = DateTime.UtcNow,
            Metadata = metadata ?? new Dictionary<string, object>()
        };
        
        _context.AuditLogs.Add(auditLog);
        await _context.SaveChangesAsync();
        
        _logger.LogInformation($"Audit log created: {entityType} {entityId} - {action}");
    }
}
