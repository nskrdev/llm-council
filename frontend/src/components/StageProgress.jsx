import './StageProgress.css';

function StageProgress({ stage1, stage2, stage3, loading }) {
  const stages = [
    {
      number: 1,
      name: 'Individual Responses',
      completed: !!stage1 && !loading?.stage1,
      active: loading?.stage1,
    },
    {
      number: 2,
      name: 'Peer Rankings',
      completed: !!stage2 && !loading?.stage2,
      active: loading?.stage2,
    },
    {
      number: 3,
      name: 'Final Synthesis',
      completed: !!stage3 && !loading?.stage3,
      active: loading?.stage3,
    },
  ];

  // Don't show if no stages are active or completed
  if (!loading && !stage1 && !stage2 && !stage3) {
    return null;
  }

  return (
    <div className="stage-progress">
      {stages.map((stage, index) => (
        <div key={stage.number} className="stage-progress-item">
          <div
            className={`stage-indicator ${stage.completed ? 'completed' : ''} ${
              stage.active ? 'active' : ''
            }`}
          >
            {stage.completed ? (
              <svg width="16" height="16" viewBox="0 0 20 20" fill="currentColor">
                <path
                  fillRule="evenodd"
                  d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"
                  clipRule="evenodd"
                />
              </svg>
            ) : stage.active ? (
              <div className="stage-spinner"></div>
            ) : (
              <span>{stage.number}</span>
            )}
          </div>
          <div className="stage-label">
            <div className="stage-name">{stage.name}</div>
            {stage.active && <div className="stage-status">In Progress...</div>}
            {stage.completed && <div className="stage-status">Complete</div>}
          </div>
          {index < stages.length - 1 && (
            <div
              className={`stage-connector ${
                stage.completed ? 'completed' : ''
              }`}
            ></div>
          )}
        </div>
      ))}
    </div>
  );
}

export default StageProgress;
