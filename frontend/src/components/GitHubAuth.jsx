import { useState, useEffect } from 'react';
import { api } from '../api';
import './GitHubAuth.css';

function GitHubAuth({ onAuthenticated }) {
  const [authState, setAuthState] = useState('checking'); // checking, unauthenticated, authenticating, authenticated
  const [userCode, setUserCode] = useState('');
  const [verificationUri, setVerificationUri] = useState('');
  const [error, setError] = useState(null);

  // Check auth status on mount
  useEffect(() => {
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const status = await api.checkGitHubAuthStatus();
      if (status.authenticated) {
        setAuthState('authenticated');
        onAuthenticated?.();
      } else {
        setAuthState('unauthenticated');
      }
    } catch (err) {
      console.error('Failed to check auth status:', err);
      setAuthState('unauthenticated');
    }
  };

  const startAuth = async () => {
    setError(null);
    setAuthState('authenticating');

    try {
      const flowData = await api.startGitHubAuth();
      setUserCode(flowData.user_code);
      setVerificationUri(flowData.verification_uri);

      // Start polling for token
      pollForToken(flowData.device_code, flowData.interval || 5);
    } catch (err) {
      setError(err.message);
      setAuthState('unauthenticated');
    }
  };

  const pollForToken = async (code, interval) => {
    const maxAttempts = 60; // 5 minutes max
    let attempts = 0;

    const poll = async () => {
      if (attempts >= maxAttempts) {
        setError('Authentication timeout. Please try again.');
        setAuthState('unauthenticated');
        return;
      }

      try {
        const result = await api.pollGitHubAuth(code);

        if (result.status === 'success') {
          setAuthState('authenticated');
          onAuthenticated?.();
        } else if (result.status === 'pending') {
          attempts++;
          setTimeout(poll, interval * 1000);
        }
      } catch (err) {
        setError(err.message);
        setAuthState('unauthenticated');
      }
    };

    poll();
  };

  const handleLogout = async () => {
    try {
      await api.logoutGitHub();
      setAuthState('unauthenticated');
      setUserCode('');
      setVerificationUri('');
    } catch (err) {
      setError(err.message);
    }
  };

  const copyCode = () => {
    navigator.clipboard.writeText(userCode);
  };

  // Loading state
  if (authState === 'checking') {
    return (
      <div className="github-auth">
        <div className="auth-checking">
          <div className="spinner"></div>
          <p>Checking authentication...</p>
        </div>
      </div>
    );
  }

  // Authenticated state
  if (authState === 'authenticated') {
    return (
      <div className="github-auth authenticated">
        <div className="auth-status">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="currentColor">
            <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
          </svg>
          <span>Connected to GitHub Copilot</span>
        </div>
        <button onClick={handleLogout} className="btn-logout">
          Logout
        </button>
      </div>
    );
  }

  // Authenticating state
  if (authState === 'authenticating') {
    return (
      <div className="github-auth authenticating">
        <div className="auth-flow">
          <h2>Authenticate with GitHub</h2>
          <div className="device-code">
            <p className="instructions">
              1. Visit{' '}
              <a href={verificationUri} target="_blank" rel="noopener noreferrer">
                {verificationUri}
              </a>
            </p>
            <p className="instructions">2. Enter this code:</p>
            <div className="code-display">
              <span className="code">{userCode}</span>
              <button onClick={copyCode} className="btn-copy" title="Copy code">
                <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
                  <path d="M4 2a2 2 0 0 1 2-2h8a2 2 0 0 1 2 2v8a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V2z" />
                  <path d="M2 6a2 2 0 0 0-2 2v6a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-2H6a2 2 0 0 1-2-2V6H2z" />
                </svg>
              </button>
            </div>
          </div>
          <div className="waiting">
            <div className="spinner"></div>
            <p>Waiting for authorization...</p>
          </div>
        </div>
      </div>
    );
  }

  // Unauthenticated state
  return (
    <div className="github-auth unauthenticated">
      <div className="auth-prompt">
        <svg width="48" height="48" viewBox="0 0 16 16" fill="currentColor">
          <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
        </svg>
        <h2>Connect to GitHub Copilot</h2>
        <p>Authenticate with your GitHub account to use your Copilot subscription.</p>
        {error && <div className="error-message">{error}</div>}
        <button onClick={startAuth} className="btn-auth">
          <svg width="16" height="16" viewBox="0 0 16 16" fill="currentColor">
            <path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27.68 0 1.36.09 2 .27 1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.013 8.013 0 0016 8c0-4.42-3.58-8-8-8z" />
          </svg>
          Login with GitHub
        </button>
        <p className="help-text">
          Requires an active GitHub Copilot subscription.{' '}
          <a href="https://github.com/settings/copilot" target="_blank" rel="noopener noreferrer">
            Manage subscription
          </a>
        </p>
      </div>
    </div>
  );
}

export default GitHubAuth;
