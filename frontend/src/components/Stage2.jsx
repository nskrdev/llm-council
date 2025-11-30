import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage2.css';

// Helper to get model info and color
function getModelInfo(modelString) {
  const [provider, model] = modelString.split('/');
  
  const providerColors = {
    claude: '#d97706',    // amber - Anthropic
    gpt: '#06b6d4',       // cyan - OpenAI  
    gemini: '#8b5cf6',    // purple - Google
    grok: '#f43f5e'       // rose - xAI
  };
  
  let color = '#6366f1';
  
  if (model) {
    const lowerModel = model.toLowerCase();
    if (lowerModel.includes('claude')) color = providerColors.claude;
    else if (lowerModel.includes('gpt') || lowerModel.includes('o1')) color = providerColors.gpt;
    else if (lowerModel.includes('gemini')) color = providerColors.gemini;
    else if (lowerModel.includes('grok')) color = providerColors.grok;
  }
  
  return { 
    shortName: model || modelString, 
    fullName: modelString,
    color 
  };
}

function deAnonymizeText(text, labelToModel) {
  if (!labelToModel) return text;

  let result = text;
  Object.entries(labelToModel).forEach(([label, model]) => {
    const modelInfo = getModelInfo(model);
    result = result.replace(new RegExp(label, 'g'), `**${modelInfo.shortName}**`);
  });
  return result;
}

export default function Stage2({ rankings, labelToModel, aggregateRankings }) {
  const [activeTab, setActiveTab] = useState('summary');

  if (!rankings || rankings.length === 0) {
    return null;
  }

  // Create voting matrix
  const models = Object.values(labelToModel || {});
  const votingMatrix = {};
  
  rankings.forEach(rank => {
    const voterModel = rank.model;
    rank.parsed_ranking?.forEach((label, position) => {
      const votedForModel = labelToModel?.[label];
      if (votedForModel) {
        if (!votingMatrix[votedForModel]) votingMatrix[votedForModel] = {};
        votingMatrix[votedForModel][voterModel] = position + 1;
      }
    });
  });

  return (
    <div className="stage stage2">
      <h3 className="stage-title">
        <span className="stage-icon">🗳️</span>
        Stage 2: Peer Review & Voting
      </h3>
      <p className="stage-description">
        Each model anonymously evaluates all responses and ranks them. 
        Models don't know which response came from which model, preventing bias.
      </p>

      <div className="stage2-tabs">
        <button
          className={`stage2-tab ${activeTab === 'summary' ? 'active' : ''}`}
          onClick={() => setActiveTab('summary')}
        >
          <span className="tab-icon">📊</span>
          Voting Summary
        </button>
        {rankings.map((rank, index) => {
          const modelInfo = getModelInfo(rank.model);
          return (
            <button
              key={index}
              className={`stage2-tab ${activeTab === rank.model ? 'active' : ''}`}
              onClick={() => setActiveTab(rank.model)}
              style={{ '--model-color': modelInfo.color }}
            >
              {modelInfo.shortName}'s Evaluation
            </button>
          );
        })}
      </div>

      {activeTab === 'summary' ? (
        <div className="voting-summary">
          <h4 className="section-title">🏆 Final Rankings</h4>
          
          {aggregateRankings && aggregateRankings.length > 0 && (
            <div className="rankings-podium">
              {aggregateRankings.map((agg, index) => {
                const modelInfo = getModelInfo(agg.model);
                const medals = ['🥇', '🥈', '🥉'];
                return (
                  <div 
                    key={index} 
                    className={`podium-card rank-${index + 1}`}
                    style={{ '--model-color': modelInfo.color }}
                  >
                    <div className="podium-rank">
                      {medals[index] || `#${index + 1}`}
                    </div>
                    <div className="podium-model" style={{ color: modelInfo.color }}>
                      {modelInfo.shortName}
                    </div>
                    <div className="podium-score">
                      Average: {agg.average_rank.toFixed(2)}
                    </div>
                    <div className="podium-votes">
                      {agg.rankings_count} votes
                    </div>
                  </div>
                );
              })}
            </div>
          )}

          <h4 className="section-title">🔤 Response Key</h4>
          <p className="section-description">
            During voting, responses were anonymized to prevent bias. Here's what each letter represents:
          </p>
          
          <div className="response-legend">
            {Object.entries(labelToModel || {}).map(([label, model], index) => {
              const modelInfo = getModelInfo(model);
              return (
                <div 
                  key={index} 
                  className="legend-item"
                  style={{ borderColor: modelInfo.color }}
                >
                  <span className="legend-label">{label}</span>
                  <span className="legend-arrow">→</span>
                  <span 
                    className="legend-model"
                    style={{ color: modelInfo.color }}
                  >
                    {modelInfo.shortName}
                  </span>
                </div>
              );
            })}
          </div>

          <h4 className="section-title">📋 Voting Matrix</h4>
          <p className="section-description">
            See how each model ranked every response (1 = best, higher = worse)
          </p>
          
          <div className="voting-matrix">
            <div className="matrix-table">
              <div className="matrix-header">
                <div className="matrix-cell matrix-corner">Model Ranked ↓ / Voter →</div>
                {rankings.map((rank, i) => {
                  const modelInfo = getModelInfo(rank.model);
                  return (
                    <div 
                      key={i} 
                      className="matrix-cell matrix-voter"
                      style={{ backgroundColor: modelInfo.color + '20', color: modelInfo.color }}
                    >
                      {modelInfo.shortName}
                    </div>
                  );
                })}
              </div>
              
              {models.map((model, i) => {
                const modelInfo = getModelInfo(model);
                return (
                  <div key={i} className="matrix-row">
                    <div 
                      className="matrix-cell matrix-model"
                      style={{ backgroundColor: modelInfo.color + '20', color: modelInfo.color }}
                    >
                      {modelInfo.shortName}
                    </div>
                    {rankings.map((rank, j) => {
                      const position = votingMatrix[model]?.[rank.model];
                      const isTopChoice = position === 1;
                      return (
                        <div 
                          key={j} 
                          className={`matrix-cell matrix-vote ${isTopChoice ? 'top-choice' : ''}`}
                        >
                          {position ? `#${position}` : '-'}
                        </div>
                      );
                    })}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      ) : (
        <div className="evaluation-detail">
          {rankings.filter(r => r.model === activeTab).map((rank, idx) => {
            const modelInfo = getModelInfo(rank.model);
            return (
              <div key={idx}>
                <div className="evaluator-header" style={{ borderColor: modelInfo.color }}>
                  <span className="evaluator-badge" style={{ backgroundColor: modelInfo.color }}>
                    {modelInfo.shortName}
                  </span>
                  <span className="evaluator-label">Full Evaluation</span>
                </div>
                
                <div className="evaluation-content markdown-content">
                  <ReactMarkdown>
                    {deAnonymizeText(rank.ranking, labelToModel)}
                  </ReactMarkdown>
                </div>

                {rank.parsed_ranking && rank.parsed_ranking.length > 0 && (
                  <div className="extracted-ranking">
                    <h5>📊 Extracted Ranking</h5>
                    <div className="ranking-list">
                      {rank.parsed_ranking.map((label, i) => {
                        const votedModel = labelToModel?.[label];
                        const votedModelInfo = votedModel ? getModelInfo(votedModel) : null;
                        return (
                          <div key={i} className="ranking-item">
                            <span className="ranking-position">#{i + 1}</span>
                            <span 
                              className="ranking-model"
                              style={{ color: votedModelInfo?.color }}
                            >
                              {votedModelInfo?.shortName || label}
                            </span>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}
