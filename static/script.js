// Enhanced Animated Background System
class EnhancedBackgroundAnimations {
    constructor() {
        this.particleContainer = document.getElementById('floatingParticles');
        this.shapesContainer = document.getElementById('geometricShapes');
        this.particles = [];
        this.shapes = [];
        this.mouseX = 0;
        this.mouseY = 0;
        this.init();
    }

    init() {
        console.log('Initializing Enhanced Background Animations...');
        console.log('Particle container:', this.particleContainer);
        console.log('Shapes container:', this.shapesContainer);
        
        this.createFloatingParticles();
        this.createGeometricShapes();
        this.addMouseInteractions();
        this.startAnimationLoop();
        
        console.log('Background animations initialized. Particles:', this.particles.length, 'Shapes:', this.shapes.length);
    }

    createFloatingParticles() {
        const particleCount = 30;
        const colors = ['#667eea', '#764ba2', '#00ffff', '#ff6b6b', '#4ecdc4', '#45b7d1', '#f093fb', '#f5576c'];
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 12 + 4; // Increased size
            const color = colors[Math.floor(Math.random() * colors.length)];
            const delay = Math.random() * 10;
            const duration = Math.random() * 6 + 8;
            
            particle.style.position = 'absolute';
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.background = `radial-gradient(circle, ${color}, transparent)`;
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = `${Math.random() * 100}%`;
            particle.style.animationName = 'floatUp';
            particle.style.animationDelay = `${delay}s`;
            particle.style.animationDuration = `${duration}s`;
            particle.style.animationIterationCount = 'infinite';
            particle.style.animationTimingFunction = 'linear';
            particle.style.boxShadow = `0 0 ${size * 3}px ${color}`;
            particle.style.borderRadius = '50%';
            particle.style.opacity = '0.9'; // Increased opacity
            
            this.particleContainer.appendChild(particle);
            this.particles.push(particle);
        }
    }

    createGeometricShapes() {
        const shapeTypes = ['circle', 'emoji-robot', 'emoji-brain'];
        const shapeCount = 25; // Increased count to accommodate emojis
        const emojis = {
            'emoji-robot': '🤖',
            'emoji-brain': '🧠'
        };
        
        console.log('Creating geometric shapes...', shapeCount);
        
        for (let i = 0; i < shapeCount; i++) {
            const shape = document.createElement('div');
            const shapeType = shapeTypes[Math.floor(Math.random() * shapeTypes.length)];
            
            if (shapeType.startsWith('emoji-')) {
                const emojiType = shapeType.split('-')[1];
                shape.className = `shape emoji ${emojiType}`;
                shape.textContent = emojis[shapeType];
                shape.style.fontSize = `${Math.random() * 20 + 30}px`; // Random size between 30-50px
                console.log(`Created emoji shape: ${emojis[shapeType]} with class: ${shape.className}`);
            } else {
                shape.className = `shape ${shapeType}`;
            }
            
            shape.style.position = 'absolute';
            shape.style.left = `${Math.random() * 100}%`;
            shape.style.top = `${Math.random() * 100}%`;
            shape.style.animationDelay = `${Math.random() * 8}s`;
            shape.style.animationDuration = `${Math.random() * 12 + 15}s`;
            
            this.shapesContainer.appendChild(shape);
            this.shapes.push(shape);
        }
        
        console.log('Shapes created:', this.shapes.length);
    }

    addMouseInteractions() {
        document.addEventListener('mousemove', (e) => {
            this.mouseX = e.clientX / window.innerWidth;
            this.mouseY = e.clientY / window.innerHeight;
            
            // Create trailing particles on mouse movement
            if (Math.random() > 0.95) {
                this.createTrailParticle(e.clientX, e.clientY);
            }
            
            // Subtle mouse-following effect for existing particles
            this.particles.forEach((particle, index) => {
                if (index % 3 === 0) {
                    const influence = 20;
                    const offsetX = (this.mouseX - 0.5) * influence;
                    const offsetY = (this.mouseY - 0.5) * influence;
                    particle.style.transform = `translate(${offsetX}px, ${offsetY}px)`;
                }
            });
        });
    }

    createTrailParticle(x, y) {
        const trail = document.createElement('div');
        trail.style.position = 'fixed';
        trail.style.left = `${x}px`;
        trail.style.top = `${y}px`;
        trail.style.width = '4px';
        trail.style.height = '4px';
        trail.style.borderRadius = '50%';
        trail.style.background = 'radial-gradient(circle, #667eea, transparent)';
        trail.style.pointerEvents = 'none';
        trail.style.zIndex = '-1';
        trail.style.animation = 'trailFade 2s ease-out forwards';
        
        document.body.appendChild(trail);
        
        setTimeout(() => {
            if (trail.parentNode) {
                trail.parentNode.removeChild(trail);
            }
        }, 2000);
    }

    startAnimationLoop() {
        setInterval(() => {
            this.refreshParticles();
        }, 10000);
        
        setInterval(() => {
            this.refreshShapes();
        }, 15000);
        
        setInterval(() => {
            this.addRandomParticle();
        }, 5000);
    }

    addRandomParticle() {
        if (this.particles.length < 40) {
            const colors = ['#667eea', '#764ba2', '#00ffff', '#ff6b6b', '#4ecdc4', '#45b7d1'];
            const particle = document.createElement('div');
            particle.className = 'particle';
            
            const size = Math.random() * 6 + 3;
            const color = colors[Math.floor(Math.random() * colors.length)];
            const duration = Math.random() * 4 + 8;
            
            particle.style.position = 'absolute';
            particle.style.width = `${size}px`;
            particle.style.height = `${size}px`;
            particle.style.background = `radial-gradient(circle, ${color}, transparent)`;
            particle.style.left = `${Math.random() * 100}%`;
            particle.style.top = '100%';
            particle.style.animationName = 'floatUp';
            particle.style.animationDuration = `${duration}s`;
            particle.style.animationIterationCount = '1';
            particle.style.animationTimingFunction = 'linear';
            particle.style.boxShadow = `0 0 ${size * 2}px ${color}`;
            particle.style.borderRadius = '50%';
            particle.style.opacity = '0.8';
            
            this.particleContainer.appendChild(particle);
            this.particles.push(particle);
            
            // Remove after animation
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                    const index = this.particles.indexOf(particle);
                    if (index > -1) {
                        this.particles.splice(index, 1);
                    }
                }
            }, duration * 1000);
        }
    }

    refreshParticles() {
        // Randomly recreate some particles for variation
        this.particles.forEach((particle, index) => {
            if (Math.random() > 0.8) {
                const colors = ['#667eea', '#764ba2', '#00ffff', '#ff6b6b', '#4ecdc4', '#45b7d1'];
                const color = colors[Math.floor(Math.random() * colors.length)];
                
                particle.style.left = `${Math.random() * 100}%`;
                particle.style.background = `radial-gradient(circle, ${color}, transparent)`;
                particle.style.boxShadow = `0 0 ${Math.random() * 15 + 5}px ${color}`;
            }
        });
    }

    refreshShapes() {
        // Randomly reposition shapes and update emoji sizes
        this.shapes.forEach(shape => {
            if (Math.random() > 0.7) {
                shape.style.left = `${Math.random() * 100}%`;
                shape.style.top = `${Math.random() * 100}%`;
                shape.style.animationDuration = `${Math.random() * 10 + 15}s`;
                
                // If it's an emoji, randomize size occasionally
                if (shape.classList.contains('emoji')) {
                    shape.style.fontSize = `${Math.random() * 20 + 20}px`;
                }
            }
        });
    }
}

// Animated Circuit Brain Background
class CircuitBrainBackground {
    constructor() {
        this.canvas = null;
        this.ctx = null;
        this.nodes = [];
        this.connections = [];
        this.animationId = null;
        this.time = 0;
        this.init();
    }

    init() {
        // Create canvas for the circuit brain background
        this.canvas = document.createElement('canvas');
        this.canvas.style.position = 'fixed';
        this.canvas.style.top = '0';
        this.canvas.style.left = '0';
        this.canvas.style.width = '100%';
        this.canvas.style.height = '100%';
        this.canvas.style.zIndex = '-1';
        this.canvas.style.opacity = '0.4';
        this.canvas.classList.add('circuit-background');
        
        this.ctx = this.canvas.getContext('2d');
        document.body.appendChild(this.canvas);
        
        this.resize();
        this.generateCircuitPattern();
        this.animate();
        
        window.addEventListener('resize', () => this.resize());
    }

    resize() {
        this.canvas.width = window.innerWidth;
        this.canvas.height = window.innerHeight;
        this.generateCircuitPattern();
    }

    generateCircuitPattern() {
        this.nodes = [];
        this.connections = [];
        
        const cols = Math.floor(this.canvas.width / 80);
        const rows = Math.floor(this.canvas.height / 80);
        
        // Generate brain-like node pattern
        for (let i = 0; i < cols; i++) {
            for (let j = 0; j < rows; j++) {
                // Create oval/brain shape
                const centerX = this.canvas.width / 2;
                const centerY = this.canvas.height / 2;
                const x = (i / cols) * this.canvas.width;
                const y = (j / rows) * this.canvas.height;
                
                const relX = (x - centerX) / (this.canvas.width * 0.3);
                const relY = (y - centerY) / (this.canvas.height * 0.4);
                
                // Brain-like oval shape with some randomness
                if (relX * relX + relY * relY <= 1 + Math.random() * 0.3) {
                    this.nodes.push({
                        x: x + (Math.random() - 0.5) * 40,
                        y: y + (Math.random() - 0.5) * 40,
                        size: 2 + Math.random() * 3,
                        pulse: Math.random() * Math.PI * 2,
                        pulseSpeed: 0.02 + Math.random() * 0.03,
                        color: this.getRandomColor(),
                        connections: []
                    });
                }
            }
        }
        
        // Create connections between nearby nodes
        for (let i = 0; i < this.nodes.length; i++) {
            const node = this.nodes[i];
            for (let j = i + 1; j < this.nodes.length; j++) {
                const other = this.nodes[j];
                const distance = Math.sqrt(
                    Math.pow(node.x - other.x, 2) + 
                    Math.pow(node.y - other.y, 2)
                );
                
                if (distance < 120 && Math.random() > 0.7) {
                    this.connections.push({
                        from: node,
                        to: other,
                        flow: Math.random(),
                        flowSpeed: 0.01 + Math.random() * 0.02,
                        opacity: 0.3 + Math.random() * 0.4
                    });
                }
            }
        }
    }

    getRandomColor() {
        const colors = [
            '#667eea',
            '#764ba2', 
            '#00ffff',
            '#ff6b6b',
            '#4ecdc4',
            '#45b7d1',
            '#96ceb4',
            '#ffd93d'
        ];
        return colors[Math.floor(Math.random() * colors.length)];
    }

    animate() {
        this.time += 0.016;
        this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
        
        // Draw connections with data flow
        this.connections.forEach(conn => {
            this.drawConnection(conn);
        });
        
        // Draw nodes with pulsing effect
        this.nodes.forEach(node => {
            this.drawNode(node);
        });
        
        this.animationId = requestAnimationFrame(() => this.animate());
    }

    drawConnection(conn) {
        const { from, to } = conn;
        
        this.ctx.beginPath();
        this.ctx.moveTo(from.x, from.y);
        this.ctx.lineTo(to.x, to.y);
        
        // Create gradient for data flow effect
        const gradient = this.ctx.createLinearGradient(from.x, from.y, to.x, to.y);
        const flowPos = (conn.flow + this.time * conn.flowSpeed) % 1;
        
        gradient.addColorStop(0, 'rgba(102, 126, 234, 0)');
        gradient.addColorStop(Math.max(0, flowPos - 0.1), 'rgba(102, 126, 234, 0)');
        gradient.addColorStop(flowPos, `rgba(102, 126, 234, ${conn.opacity})`);
        gradient.addColorStop(Math.min(1, flowPos + 0.1), 'rgba(102, 126, 234, 0)');
        gradient.addColorStop(1, 'rgba(102, 126, 234, 0)');
        
        this.ctx.strokeStyle = gradient;
        this.ctx.lineWidth = 1;
        this.ctx.stroke();
    }

    drawNode(node) {
        const pulseSize = node.size + Math.sin(this.time * node.pulseSpeed + node.pulse) * 1.5;
        const alpha = 0.6 + Math.sin(this.time * node.pulseSpeed + node.pulse) * 0.4;
        
        // Draw glow effect
        this.ctx.beginPath();
        this.ctx.arc(node.x, node.y, pulseSize * 2, 0, Math.PI * 2);
        this.ctx.fillStyle = `${node.color}20`;
        this.ctx.fill();
        
        // Draw main node
        this.ctx.beginPath();
        this.ctx.arc(node.x, node.y, pulseSize, 0, Math.PI * 2);
        this.ctx.fillStyle = node.color + Math.floor(alpha * 255).toString(16).padStart(2, '0');
        this.ctx.fill();
    }

    destroy() {
        if (this.animationId) {
            cancelAnimationFrame(this.animationId);
        }
        if (this.canvas && this.canvas.parentNode) {
            this.canvas.parentNode.removeChild(this.canvas);
        }
    }
}

class AICMSClient {
    constructor() {
        this.ws = null;
        this.isConnected = false;
        this.currentWorkspace = '/home/dinochlai/interactive-cms';
        this.reconnectAttempts = 0;
        this.maxReconnectAttempts = 5;
        this.isAIProcessing = false;
        this.loadingMessageElement = null;
        this.connect();
    }

    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws`;
        
        this.ws = new WebSocket(wsUrl);
        
        this.ws.onopen = () => {
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.updateConnectionStatus();
            this.addSystemMessage('Connected to AI CMS server');
        };
        
        this.ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.ws.onclose = () => {
            this.isConnected = false;
            this.updateConnectionStatus();
            // Remove loading message if connection is lost
            this.removeLoadingMessage();
            this.addSystemMessage('Disconnected from server');
            this.attemptReconnect();
        };
        
        this.ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            // Remove loading message on connection error
            this.removeLoadingMessage();
            this.addSystemMessage('Connection error occurred', 'error');
        };
    }

    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            const delay = Math.pow(2, this.reconnectAttempts) * 1000;
            
            this.addSystemMessage(`Attempting to reconnect in ${delay/1000} seconds... (${this.reconnectAttempts}/${this.maxReconnectAttempts})`);
            
            setTimeout(() => {
                this.connect();
            }, delay);
        }
    }

    sendMessage(type, data) {
        if (this.isConnected && this.ws.readyState === WebSocket.OPEN) {
            this.ws.send(JSON.stringify({
                type: type,
                workspace: this.currentWorkspace,
                ...data
            }));
        } else {
            this.addSystemMessage('Not connected to server', 'error');
        }
    }

    handleMessage(data) {
        switch (data.type) {
            case 'ai_response':
                this.handleAIResponse(data);
                break;
            case 'conversation_cleared':
                this.handleConversationCleared(data);
                break;
            case 'conversation_history':
                this.handleConversationHistory(data);
                break;
            case 'error':
                // Remove loading message on error
                this.removeLoadingMessage();
                this.addSystemMessage(data.message || 'Unknown error occurred', 'error');
                break;
            default:
                console.log('Unknown message type:', data.type);
        }
    }

    handleAIResponse(data) {
        // Remove loading message
        this.removeLoadingMessage();
        
        const result = data.result;
        let responseText = '';
        
        console.log('AI Response received:', result);
        
        if (result.success) {
            responseText = result.stdout || 'AI response received successfully';
            
            // Clean up any remaining escape characters and formatting
            responseText = responseText
                .replace(/\\n/g, '\n')
                .replace(/\\"/g, '"')
                .trim();
                
            // If response is empty, show a default message
            if (!responseText || responseText.length < 3) {
                responseText = "I'm here to help! Please ask me a specific question or request assistance with coding, explanations, or any other task.";
            }
                
        } else {
            responseText = result.error || result.stderr || 'AI command failed';
            
            // Check if it's an API key issue
            if (responseText.includes('API key') || responseText.includes('authentication')) {
                responseText = "⚠️ AI service configuration needed. Please check your API keys in the backend configuration.";
            }
        }
        
        this.addAIMessage(responseText);
    }



    handleConversationCleared(data) {
        this.addSystemMessage('✓ Conversation history cleared on server', 'info');
    }

    handleConversationHistory(data) {
        const history = data.history || [];
        if (history.length === 0) {
            this.addSystemMessage('No conversation history found', 'info');
            return;
        }
        
        this.addSystemMessage(`📝 Conversation History (${history.length} messages):`, 'info');
        history.forEach((msg, index) => {
            const timestamp = new Date(msg.timestamp).toLocaleTimeString();
            const content = msg.content.length > 100 ? msg.content.substring(0, 100) + '...' : msg.content;
            this.addSystemMessage(`${index + 1}. [${timestamp}] ${msg.role}: ${content}`, 'info');
        });
    }

    addChatMessage(content, isUser = false) {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${isUser ? 'user-message' : 'ai-message'}`;
        messageDiv.textContent = content;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }

    addAIMessage(content) {
        this.addChatMessage(content, false);
    }

    addLoadingMessage() {
        if (this.loadingMessageElement) return; // Prevent multiple loading messages
        
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message loading-message';
        messageDiv.innerHTML = '🤖 AI is working<span class="loading-dots"></span>';
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        this.loadingMessageElement = messageDiv;
        this.isAIProcessing = true;
        
        // Update button state
        this.updateSendButtonState(true);
    }

    removeLoadingMessage() {
        if (this.loadingMessageElement) {
            this.loadingMessageElement.remove();
            this.loadingMessageElement = null;
        }
        this.isAIProcessing = false;
        
        // Update button state
        this.updateSendButtonState(false);
    }

    updateSendButtonState(isProcessing) {
        const sendButton = document.getElementById('sendAIButton');
        if (sendButton) {
            if (isProcessing) {
                sendButton.disabled = true;
                sendButton.textContent = 'Processing...';
                sendButton.style.opacity = '0.6';
                sendButton.style.cursor = 'not-allowed';
            } else {
                sendButton.disabled = false;
                sendButton.textContent = 'Send to AI';
                sendButton.style.opacity = '1';
                sendButton.style.cursor = 'pointer';
            }
        }
    }

    addSystemMessage(content, type = 'info') {
        const messagesContainer = document.getElementById('chatMessages');
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message system-message';
        messageDiv.textContent = content;
        messagesContainer.appendChild(messageDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }



    updateConnectionStatus() {
        const statusElement = document.getElementById('connectionStatus');
        if (this.isConnected) {
            statusElement.textContent = 'Connected';
            statusElement.className = 'connection-status connected';
        } else {
            statusElement.textContent = 'Disconnected';
            statusElement.className = 'connection-status disconnected';
        }
    }
}

// Initialize the client
const aiCMS = new AICMSClient();

// UI Functions
function sendAIMessage() {
    const input = document.getElementById('chatInput');
    const autoSaveCheckbox = document.getElementById('autoSaveChat');
    let message = input.value.trim();
    
    if (!message) return;
    
    // Prevent sending multiple messages while AI is processing
    if (aiCMS.isAIProcessing) {
        aiCMS.addSystemMessage('⚠️ Please wait for the AI to finish processing your previous request.', 'warning');
        return;
    }
    
    aiCMS.addChatMessage(input.value, true); // Show original message to user
    aiCMS.addLoadingMessage();
    aiCMS.sendMessage('ai_chat', { 
        prompt: message,
        auto_save: autoSaveCheckbox ? autoSaveCheckbox.checked : true
    });
    
    input.value = '';
}



function clearChat() {
    const messagesContainer = document.getElementById('chatMessages');
    messagesContainer.innerHTML = '<div class="message system-message">Chat cleared. Start a new conversation!</div>';
    
    // Send clear conversation command to backend
    aiCMS.sendMessage('clear_conversation', {});
}

function viewConversationHistory() {
    // Request conversation history from backend
    aiCMS.sendMessage('get_conversation_history', {});
}

// Event listeners
document.getElementById('chatInput').addEventListener('keypress', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendAIMessage();
    }
});

// Initialize the animated backgrounds
let circuitBackground;
let enhancedBackground;
document.addEventListener('DOMContentLoaded', function() {
    circuitBackground = new CircuitBrainBackground();
    enhancedBackground = new EnhancedBackgroundAnimations();
});

// Global function to test emoji creation (accessible from browser console)
function testEmojis() {
    if (enhancedBackground) {
        enhancedBackground.testEmojiCreation();
    } else {
        console.log('Enhanced background not initialized yet');
    }
}

// Clean up background when page unloads
window.addEventListener('beforeunload', function() {
    if (circuitBackground) {
        circuitBackground.destroy();
    }
});
