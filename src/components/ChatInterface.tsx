import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Lightbulb } from 'lucide-react';

interface Message {
  id: string;
  type: 'user' | 'bot';
  content: string;
  timestamp: Date;
}

const ChatInterface: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'bot',
      content: 'Hello! I\'m your AI career coach. I can help you with LinkedIn optimization, career advice, job search strategies, and professional development. What would you like to discuss today?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    // Simulate AI response
    setTimeout(() => {
      const botResponse = generateBotResponse(inputMessage);
      const botMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'bot',
        content: botResponse,
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, botMessage]);
      setIsTyping(false);
    }, 1500);
  };

  const generateBotResponse = (userInput: string): string => {
    const input = userInput.toLowerCase();
    
    if (input.includes('linkedin') && input.includes('headline')) {
      return `Great question about LinkedIn headlines! Here are some tips for creating a compelling headline:

1. **Include your target role**: Be specific about what you do
2. **Add key skills**: Mention 2-3 relevant technologies or skills
3. **Show value**: What do you help companies achieve?
4. **Use keywords**: Include terms recruiters search for
5. **Keep it under 220 characters**

Example: "Senior Full Stack Developer | React & Node.js Expert | Building Scalable Web Applications | Helping Startups Grow"

Would you like me to help you craft a specific headline for your profile?`;
    }
    
    if (input.includes('job') && (input.includes('search') || input.includes('hunting'))) {
      return `Job searching can be challenging, but here's a strategic approach:

**1. Optimize Your Foundation**
- Update LinkedIn profile with keywords
- Prepare 2-3 versions of your resume
- Build a portfolio showcasing your best work

**2. Target Your Search**
- Identify 10-15 companies you'd love to work for
- Research their tech stack and culture
- Follow them on LinkedIn and engage with their content

**3. Network Strategically**
- Reach out to employees at target companies
- Attend industry meetups and virtual events
- Ask for informational interviews

**4. Apply Smart**
- Tailor each application to the specific role
- Apply within 24-48 hours of job posting
- Follow up after 1-2 weeks

What specific aspect of job searching would you like to dive deeper into?`;
    }
    
    if (input.includes('skill') && (input.includes('learn') || input.includes('develop'))) {
      return `Skill development is crucial for career growth! Here's how to approach it strategically:

**1. Identify Market Demand**
- Research job postings in your target role
- Check LinkedIn skill assessments
- Look at industry trend reports

**2. Create a Learning Plan**
- Start with high-impact skills first
- Mix theoretical learning with hands-on practice
- Set specific, measurable goals

**3. Popular Skills by Role:**
- **Frontend**: React, TypeScript, Next.js, Tailwind CSS
- **Backend**: Node.js, Python, PostgreSQL, AWS
- **Full Stack**: All of the above plus system design
- **Leadership**: Project management, team communication, mentoring

**4. Learning Resources**
- Online courses (Udemy, Coursera, Pluralsight)
- Documentation and official tutorials
- Open source contributions
- Personal projects

What specific skills are you looking to develop?`;
    }
    
    if (input.includes('interview')) {
      return `Interview preparation is key to landing your dream job! Here's a comprehensive approach:

**Technical Interviews:**
- Practice coding problems on LeetCode/HackerRank
- Review system design concepts
- Prepare to explain your past projects in detail
- Practice whiteboarding (even virtually)

**Behavioral Interviews:**
- Use the STAR method (Situation, Task, Action, Result)
- Prepare 5-7 stories showcasing different skills
- Research the company culture and values
- Prepare thoughtful questions about the role and team

**Common Questions to Prepare:**
- "Tell me about yourself"
- "Why do you want to work here?"
- "Describe a challenging project you worked on"
- "How do you handle conflict in a team?"

**Day of Interview:**
- Test your tech setup beforehand
- Have questions ready to ask them
- Bring copies of your resume
- Follow up within 24 hours

Would you like me to help you prepare for any specific type of interview question?`;
    }
    
    // Default responses for general queries
    const responses = [
      `That's an interesting question! Based on current industry trends, I'd recommend focusing on building a strong foundation in both technical skills and soft skills. 

For technical growth, consider:
- Staying updated with the latest frameworks and tools
- Contributing to open source projects
- Building a portfolio that showcases real-world problem solving

For career development:
- Networking within your industry
- Seeking mentorship opportunities
- Developing leadership and communication skills

What specific area would you like to explore further?`,
      
      `Great point! In today's competitive job market, it's important to differentiate yourself. Here are some strategies:

1. **Develop a unique skill combination** - Don't just be a "React developer," be a "React developer with UX design skills"
2. **Build in public** - Share your learning journey on LinkedIn and Twitter
3. **Contribute to the community** - Write blog posts, speak at meetups, help others
4. **Focus on business impact** - Always tie your technical work to business outcomes

The key is to be authentic and consistent in your professional brand. What aspect of personal branding interests you most?`,
      
      `Excellent question! Career transitions can be challenging but very rewarding. Here's how to approach it:

**1. Assess Your Transferable Skills**
- Identify skills that apply to your target role
- Highlight relevant experience, even if from different industries
- Focus on problem-solving abilities and learning agility

**2. Bridge the Gap**
- Take online courses in your target field
- Work on relevant side projects
- Volunteer or freelance in the new area
- Network with professionals in the target industry

**3. Tell Your Story**
- Craft a compelling narrative about why you're making the change
- Show passion and commitment to the new field
- Demonstrate how your unique background adds value

What type of career transition are you considering?`
    ];
    
    return responses[Math.floor(Math.random() * responses.length)];
  };

  const suggestedQuestions = [
    "How can I improve my LinkedIn headline?",
    "What skills should I learn for career growth?",
    "How do I prepare for technical interviews?",
    "What's the best job search strategy?"
  ];

  const handleSuggestedQuestion = (question: string) => {
    setInputMessage(question);
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Career Coach Chat</h2>
        
        {/* Chat Messages */}
        <div className="h-96 overflow-y-auto border border-gray-200 rounded-lg p-4 mb-4 space-y-4">
          {messages.map((message) => (
            <div
              key={message.id}
              className={`flex ${message.type === 'user' ? 'justify-end' : 'justify-start'}`}
            >
              <div className={`flex space-x-2 max-w-xs lg:max-w-md ${
                message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
              }`}>
                <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
                  message.type === 'user' ? 'bg-blue-600' : 'bg-gray-600'
                }`}>
                  {message.type === 'user' ? 
                    <User className="h-4 w-4 text-white" /> : 
                    <Bot className="h-4 w-4 text-white" />
                  }
                </div>
                <div className={`px-4 py-2 rounded-lg ${
                  message.type === 'user' 
                    ? 'bg-blue-600 text-white' 
                    : 'bg-gray-100 text-gray-900'
                }`}>
                  <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                  <p className="text-xs mt-1 opacity-70">
                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                  </p>
                </div>
              </div>
            </div>
          ))}
          
          {isTyping && (
            <div className="flex justify-start">
              <div className="flex space-x-2 max-w-xs lg:max-w-md">
                <div className="flex-shrink-0 w-8 h-8 bg-gray-600 rounded-full flex items-center justify-center">
                  <Bot className="h-4 w-4 text-white" />
                </div>
                <div className="bg-gray-100 px-4 py-2 rounded-lg">
                  <div className="flex space-x-1">
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                    <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
                  </div>
                </div>
              </div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Suggested Questions */}
        {messages.length === 1 && (
          <div className="mb-4">
            <div className="flex items-center space-x-2 mb-2">
              <Lightbulb className="h-4 w-4 text-yellow-600" />
              <span className="text-sm font-medium text-gray-700">Suggested questions:</span>
            </div>
            <div className="flex flex-wrap gap-2">
              {suggestedQuestions.map((question, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestedQuestion(question)}
                  className="px-3 py-1 bg-blue-100 text-blue-700 rounded-full text-sm hover:bg-blue-200 transition-colors"
                >
                  {question}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Message Input */}
        <div className="flex space-x-2">
          <input
            type="text"
            value={inputMessage}
            onChange={(e) => setInputMessage(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
            placeholder="Ask me anything about your career..."
            className="flex-1 px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          />
          <button
            onClick={handleSendMessage}
            disabled={!inputMessage.trim() || isTyping}
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Send className="h-4 w-4" />
          </button>
        </div>
      </div>
    </div>
  );
};

export default ChatInterface;