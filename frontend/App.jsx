import React, { useState, useEffect } from 'react';
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8000';

const INDIAN_LANGUAGES = [
  { code: 'hi-IN', name: 'Hindi' },
  { code: 'ta-IN', name: 'Tamil' },
  { code: 'te-IN', name: 'Telugu' },
  { code: 'kn-IN', name: 'Kannada' },
  { code: 'ml-IN', name: 'Malayalam' },
  { code: 'bn-IN', name: 'Bengali' },
  { code: 'gu-IN', name: 'Gujarati' },
  { code: 'mr-IN', name: 'Marathi' },
  { code: 'en-IN', name: 'English (Indian)' }
];

const LLM_MODELS = [
  { id: 'groq-mixtral', name: 'Groq Mixtral 8x7B', provider: 'groq' },
  { id: 'groq-llama2', name: 'Groq Llama 2 70B', provider: 'groq' },
  { id: 'gpt-4', name: 'OpenAI GPT-4', provider: 'openai', paid: true },
  { id: 'claude-3', name: 'Anthropic Claude 3', provider: 'anthropic', paid: true }
];

const TTS_MODELS = [
 { id: 'google-tts', name: 'Google Cloud TTS', provider: 'google', free: true },
 { id: 'elevenlabs-v2', name: 'ElevenLabs V2', provider: 'elevenlabs', free: false },
 { id: 'replicate-xtts', name: 'Replicate XTTS', provider: 'replicate', free: true },
 { id: 'azure-speech', name: 'Azure Speech', provider: 'azure', free: false },
 { id: 'cartesia', name: 'Cartesia', provider: 'cartesia', free: false }
];

const STT_MODELS = [
 { id: 'google-stt', name: 'Google Cloud Speech-to-Text', provider: 'google', free: true },
 { id: 'openai-whisper', name: 'OpenAI Whisper', provider: 'openai', free: false },
 { id: 'groq-whisper', name: 'Groq Whisper', provider: 'groq', free: true },
 { id: 'assemblyai', name: 'AssemblyAI', provider: 'assemblyai', free: false },
 { id: 'deepgram', name: 'Deepgram', provider: 'deepgram', free: false },
 { id: 'azure-stt', name: 'Azure Speech Recognition', provider: 'azure', free: false }
];

export default function App() {
  const [agents, setAgents] = useState([]);
  const [formData, setFormData] = useState({
    name: '',
    role: '',
    systemInstruction: '',
    language: 'hi-IN',
    llmModel: 'groq-mixtral',
    ttsVoice: 'default-indian',
 ttsModel: 'google-tts',
 sttModel: 'google-stt'
  });
  const [voiceFile, setVoiceFile] = useState(null);
  const [voiceLibrary, setVoiceLibrary] = useState([]);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState('');

  useEffect(() => {
    fetchAgents();
    fetchVoiceLibrary();
  }, []);

  const fetchAgents = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/agents`);
      setAgents(response.data);
    } catch (error) {
      console.error('Error fetching agents:', error);
    }
  };

  const fetchVoiceLibrary = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/api/voices`);
      setVoiceLibrary(response.data);
    } catch (error) {
      console.error('Error fetching voices:', error);
    }
  };

  const handleCreateAgent = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/api/agents`, {
        ...formData,
        voiceId: formData.ttsVoice
      });
      setMessage('Agent created successfully!');
      setFormData({
        name: '',
        role: '',
        systemInstruction: '',
        language: 'hi-IN',
        llmModel: 'groq-mixtral',
        ttsVoice: 'default-indian'
      });
      fetchAgents();
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error creating agent: ' + error.message);
    }
    setLoading(false);
  };

  const handleVoiceUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    const formDataUpload = new FormData();
    formDataUpload.append('voice_sample', file);
    formDataUpload.append('voice_name', `cloned-voice-${Date.now()}`);

    setLoading(true);
    try {
      const response = await axios.post(
        `${API_BASE_URL}/api/voices/clone`,
        formDataUpload,
        { headers: { 'Content-Type': 'multipart/form-data' } }
      );
      setMessage('Voice cloned successfully!');
      fetchVoiceLibrary();
      setTimeout(() => setMessage(''), 3000);
    } catch (error) {
      setMessage('Error cloning voice: ' + error.message);
    }
    setLoading(false);
  };

  return (
    <div style={styles.container}>
      <header style={styles.header}>
        <h1>🎙️ Indian Voice Agent Builder</h1>
        <p>Create AI voice agents in any Indian language with your cloned voice</p>
      </header>

      <main style={styles.main}>
        <section style={styles.section}>
          <h2>📝 Create New Agent</h2>
          <form onSubmit={handleCreateAgent} style={styles.form}>
            <div style={styles.formGroup}>
              <label>Agent Name</label>
              <input
                type="text"
                placeholder="e.g., Customer Support Bot"
                value={formData.name}
                onChange={(e) => setFormData({ ...formData, name: e.target.value })}
                required
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label>Agent Role</label>
              <input
                type="text"
                placeholder="e.g., Sales Representative"
                value={formData.role}
                onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                required
                style={styles.input}
              />
            </div>

            <div style={styles.formGroup}>
              <label>System Instruction</label>
              <textarea
                placeholder="Define how the agent should behave and respond"
                value={formData.systemInstruction}
                onChange={(e) => setFormData({ ...formData, systemInstruction: e.target.value })}
                required
                style={styles.textarea}
              />
            </div>

            <div style={styles.formRow}>
              <div style={styles.formGroup}>
                <label>Language</label>
                <select
                  value={formData.language}
                  onChange={(e) => setFormData({ ...formData, language: e.target.value })}
                  style={styles.select}
                >
                  {INDIAN_LANGUAGES.map(lang => (
                    <option key={lang.code} value={lang.code}>
                      {lang.name}
                    </option>
                  ))}
                </select>
              </div>

              <div style={styles.formGroup}>
                <label>LLM Model</label>
                <select
                  value={formData.llmModel}
                  onChange={(e) => setFormData({ ...formData, llmModel: e.target.value })}
                  style={styles.select}
                >
                  {LLM_MODELS.map(model => (
                    <option key={model.id} value={model.id}>
                      {model.name} {model.paid ? '(Paid)' : '(Free)'}
                    </option>
                  ))}
                </select>
                
 <div style={styles.formRow}>
 <div style={styles.formGroup}>
 <label>TTS Model</label>
 <select
 value={formData.ttsModel}
 onChange={(e) => setFormData({ ...formData, ttsModel: e.target.value })}
 style={styles.select}
 >
 {TTS_MODELS.map(model => (
 <option key={model.id} value={model.id}>
 {model.name} {model.free ? '(Free)' : '(Paid)'}
 </option>
 ))}
 </select>
 </div>

 <div style={styles.formGroup}>
 <label>STT Model</label>
 <select
 value={formData.sttModel}
 onChange={(e) => setFormData({ ...formData, sttModel: e.target.value })}
 style={styles.select}
 >
 {STT_MODELS.map(model => (
 <option key={model.id} value={model.id}>
 {model.name} {model.free ? '(Free)' : '(Paid)'}
 </option>
 ))}
 </select>
 </div>
 </div>
              </div>
            </div>

            <button type="submit" disabled={loading} style={styles.button}>
              {loading ? 'Creating...' : '✨ Create Agent'}
            </button>
          </form>
        </section>

        <section style={styles.section}>
          <h2>🎵 Voice Cloning</h2>
          <div style={styles.voiceUpload}>
            <input
              type="file"
              accept="audio/*"
              onChange={handleVoiceUpload}
              disabled={loading}
              style={styles.fileInput}
            />
            <p>Upload 2-5 minute voice sample (WAV, MP3, OGG)</p>
          </div>
        </section>

        <section style={styles.section}>
          <h2>📚 Your Agents ({agents.length})</h2>
          {agents.length === 0 ? (
            <p>No agents created yet. Create your first agent above!</p>
          ) : (
            <div style={styles.agentsList}>
              {agents.map(agent => (
                <div key={agent.id} style={styles.agentCard}>
                  <h3>{agent.name}</h3>
                  <p><strong>Role:</strong> {agent.role}</p>
                  <p><strong>Language:</strong> {agent.language}</p>
                  <p><strong>Model:</strong> {agent.llmModel}</p>
                </div>
              ))}
            </div>
          )}
        </section>

        {message && <div style={styles.message}>{message}</div>}
      </main>
    </div>
  );
}

const styles = {
  container: {
    fontFamily: 'system-ui, -apple-system, sans-serif',
    backgroundColor: '#0f172a',
    color: '#e2e8f0',
    minHeight: '100vh',
    padding: '20px'
  },
  header: {
    textAlign: 'center',
    marginBottom: '40px',
    borderBottom: '2px solid #3b82f6',
    paddingBottom: '20px'
  },
  main: {
    maxWidth: '1200px',
    margin: '0 auto'
  },
  section: {
    backgroundColor: '#1e293b',
    borderRadius: '8px',
    padding: '24px',
    marginBottom: '24px',
    border: '1px solid #334155'
  },
  form: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  formGroup: {
    display: 'flex',
    flexDirection: 'column',
    gap: '8px'
  },
  formRow: {
    display: 'grid',
    gridTemplateColumns: '1fr 1fr',
    gap: '16px'
  },
  input: {
    padding: '12px',
    borderRadius: '6px',
    border: '1px solid #475569',
    backgroundColor: '#0f172a',
    color: '#e2e8f0',
    fontSize: '14px'
  },
  textarea: {
    padding: '12px',
    borderRadius: '6px',
    border: '1px solid #475569',
    backgroundColor: '#0f172a',
    color: '#e2e8f0',
    fontSize: '14px',
    minHeight: '100px',
    fontFamily: 'monospace'
  },
  select: {
    padding: '12px',
    borderRadius: '6px',
    border: '1px solid #475569',
    backgroundColor: '#0f172a',
    color: '#e2e8f0',
    fontSize: '14px'
  },
  button: {
    padding: '12px 24px',
    borderRadius: '6px',
    border: 'none',
    backgroundColor: '#3b82f6',
    color: 'white',
    fontSize: '16px',
    fontWeight: 'bold',
    cursor: 'pointer',
    marginTop: '16px',
    transition: 'background-color 0.3s'
  },
  voiceUpload: {
    textAlign: 'center',
    padding: '40px'
  },
  fileInput: {
    padding: '12px',
    cursor: 'pointer'
  },
  agentsList: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fill, minmax(300px, 1fr))',
    gap: '16px'
  },
  agentCard: {
    backgroundColor: '#0f172a',
    padding: '16px',
    borderRadius: '6px',
    border: '1px solid #475569'
  },
  message: {
    position: 'fixed',
    top: '20px',
    right: '20px',
    backgroundColor: '#10b981',
    padding: '16px 24px',
    borderRadius: '6px',
    color: 'white'
  }
};
