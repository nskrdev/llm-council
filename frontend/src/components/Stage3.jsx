import ReactMarkdown from 'react-markdown';
import './Stage3.css';

// Helper to get model info and color
function getModelInfo(modelString) {
  const [, model] = modelString.split('/');
  
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

export default function Stage3({ finalResponse }) {
  if (!finalResponse) {
    return null;
  }

  const chairmanInfo = getModelInfo(finalResponse.model);
  const isError = finalResponse.response.includes('Error:');

  return (
    <div className="stage stage3">
      <h3 className="stage-title">
        <span className="stage-icon">⚖️</span>
        Stage 3: Chairman's Final Answer
      </h3>
      <p className="stage-description">
        The chairman reviews all responses and peer evaluations to synthesize the best possible answer.
      </p>

      <div className="chairman-card">
        <div 
          className="chairman-header" 
          style={{ 
            borderColor: chairmanInfo.color,
            background: `linear-gradient(135deg, ${chairmanInfo.color}15 0%, ${chairmanInfo.color}05 100%)`
          }}
        >
          <div className="chairman-badge-section">
            <span 
              className="chairman-badge" 
              style={{ backgroundColor: chairmanInfo.color }}
            >
              👔 Chairman
            </span>
            <span className="chairman-model" style={{ color: chairmanInfo.color }}>
              {chairmanInfo.shortName}
            </span>
          </div>
          <div className="chairman-meta">
            <span className="meta-label">Decision Authority</span>
          </div>
        </div>

        {isError ? (
          <div className="error-message">
            <span className="error-icon">⚠️</span>
            <div>
              <div className="error-title">Unable to Generate Final Synthesis</div>
              <div className="error-details">
                The chairman encountered an issue. Please refer to the individual responses and peer rankings above.
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="final-answer-section">
              <h4 className="final-answer-label">
                <span className="answer-icon">💡</span>
                Final Council Answer
              </h4>
              <div className="final-answer-content markdown-content">
                <ReactMarkdown>{finalResponse.response}</ReactMarkdown>
              </div>
            </div>

            <div className="synthesis-info">
              <div className="info-icon">ℹ️</div>
              <div className="info-text">
                <strong>Why this answer?</strong> The chairman synthesized insights from all {finalResponse.response.includes('four') || finalResponse.response.includes('4') ? '4' : ''} council members, 
                considering their individual responses, peer evaluations, and the consensus rankings to provide 
                the most comprehensive and accurate answer.
              </div>
            </div>
          </>
        )}
      </div>
    </div>
  );
}
