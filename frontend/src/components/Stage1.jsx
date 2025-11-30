import { useState } from 'react';
import ReactMarkdown from 'react-markdown';
import './Stage1.css';

// Helper to get model provider and color
function getModelInfo(modelString) {
  const [provider, model] = modelString.split('/');
  const colors = {
    github: '#6366f1', // indigo
    openrouter: '#10b981' // emerald
  };
  
  const providerColors = {
    claude: '#d97706',    // amber - Anthropic
    gpt: '#06b6d4',       // cyan - OpenAI  
    gemini: '#8b5cf6',    // purple - Google
    grok: '#f43f5e'       // rose - xAI
  };
  
  let color = colors[provider] || '#6366f1';
  
  // Check model name for specific provider
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

export default function Stage1({ responses }) {
  const [activeTab, setActiveTab] = useState(0);

  if (!responses || responses.length === 0) {
    return null;
  }

  const activeModel = getModelInfo(responses[activeTab].model);

  return (
    <div className="stage stage1">
      <h3 className="stage-title">
        <span className="stage-icon">💭</span>
        Stage 1: Individual Responses
      </h3>
      <p className="stage-description">
        Each council member provides their independent answer to your question.
      </p>

      <div className="model-tabs">
        {responses.map((resp, index) => {
          const modelInfo = getModelInfo(resp.model);
          return (
            <button
              key={index}
              className={`model-tab ${activeTab === index ? 'active' : ''}`}
              onClick={() => setActiveTab(index)}
              style={{
                '--model-color': modelInfo.color
              }}
            >
              <span className="model-tab-name">{modelInfo.shortName}</span>
            </button>
          );
        })}
      </div>

      <div className="response-card">
        <div className="response-header" style={{ borderColor: activeModel.color }}>
          <span className="model-badge" style={{ backgroundColor: activeModel.color }}>
            {activeModel.shortName}
          </span>
          <span className="model-fullname">{activeModel.fullName}</span>
        </div>
        <div className="response-content markdown-content">
          <ReactMarkdown>{responses[activeTab].response}</ReactMarkdown>
        </div>
      </div>
    </div>
  );
}
