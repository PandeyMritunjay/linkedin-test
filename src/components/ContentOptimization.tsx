import React, { useState } from 'react';
import { Edit3, Sparkles, Copy, Check } from 'lucide-react';

const ContentOptimization: React.FC = () => {
  const [selectedSection, setSelectedSection] = useState('headline');
  const [currentContent, setCurrentContent] = useState('');
  const [targetRole, setTargetRole] = useState('');
  const [isOptimizing, setIsOptimizing] = useState(false);
  const [optimizedContent, setOptimizedContent] = useState('');
  const [copied, setCopied] = useState(false);

  const sections = [
    { id: 'headline', label: 'Professional Headline', placeholder: 'Enter your current headline...' },
    { id: 'summary', label: 'About Section', placeholder: 'Enter your current about section...' },
    { id: 'experience', label: 'Job Description', placeholder: 'Enter a job description...' }
  ];

  const handleOptimize = async () => {
    if (!currentContent.trim()) return;
    
    setIsOptimizing(true);
    
    // Simulate API call with mock optimized content
    setTimeout(() => {
      let optimized = '';
      
      if (selectedSection === 'headline') {
        optimized = `🚀 Senior Full Stack Developer | React & Node.js Expert | Building Scalable Web Applications | ${targetRole || 'Tech Innovation'} Enthusiast`;
      } else if (selectedSection === 'summary') {
        optimized = `Passionate Full Stack Developer with 5+ years of experience crafting exceptional digital experiences. Specialized in React, Node.js, and modern web technologies.

🔧 Core Expertise:
• Frontend: React, TypeScript, Next.js, Tailwind CSS
• Backend: Node.js, Express, Python, RESTful APIs
• Database: PostgreSQL, MongoDB, Redis
• Cloud: AWS, Docker, CI/CD pipelines

💡 What I Bring:
✅ Led development of 15+ web applications serving 100K+ users
✅ Reduced application load times by 40% through optimization
✅ Mentored junior developers and established coding standards
✅ Strong advocate for clean code and test-driven development

🎯 Currently seeking opportunities in ${targetRole || 'innovative tech companies'} where I can leverage my technical expertise to drive product growth and team success.

Let's connect and discuss how I can contribute to your next big project! 🚀`;
      } else {
        optimized = `• Developed and maintained 10+ responsive web applications using React, Node.js, and TypeScript
• Collaborated with cross-functional teams of 8+ members to deliver projects 20% ahead of schedule
• Implemented automated testing strategies that reduced bugs by 35% and improved code quality
• Optimized database queries and API performance, resulting in 50% faster page load times
• Mentored 3 junior developers and conducted code reviews to maintain high development standards
• Integrated third-party APIs and payment systems, increasing user engagement by 25%`;
      }
      
      setOptimizedContent(optimized);
      setIsOptimizing(false);
    }, 2000);
  };

  const handleCopy = async () => {
    await navigator.clipboard.writeText(optimizedContent);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const sampleContent = {
    headline: 'Software Developer at Tech Company',
    summary: 'I am a software developer with experience in web development. I work with JavaScript and have built several applications.',
    experience: 'Worked on various web development projects. Used JavaScript and other technologies to build applications.'
  };

  const handleUseSample = () => {
    setCurrentContent(sampleContent[selectedSection as keyof typeof sampleContent]);
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Content Optimization</h2>
        
        <div className="space-y-4">
          {/* Section Selection */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Select Section to Optimize
            </label>
            <select
              value={selectedSection}
              onChange={(e) => setSelectedSection(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            >
              {sections.map((section) => (
                <option key={section.id} value={section.id}>
                  {section.label}
                </option>
              ))}
            </select>
          </div>

          {/* Target Role */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Target Role (Optional)
            </label>
            <input
              type="text"
              value={targetRole}
              onChange={(e) => setTargetRole(e.target.value)}
              placeholder="e.g., Senior Frontend Developer, Product Manager"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          {/* Current Content */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Current Content
            </label>
            <textarea
              value={currentContent}
              onChange={(e) => setCurrentContent(e.target.value)}
              placeholder={sections.find(s => s.id === selectedSection)?.placeholder}
              rows={selectedSection === 'summary' ? 6 : 3}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleOptimize}
              disabled={!currentContent.trim() || isOptimizing}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <Sparkles className="h-4 w-4" />
              <span>{isOptimizing ? 'Optimizing...' : 'Optimize Content'}</span>
            </button>
            <button
              onClick={handleUseSample}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              Use Sample
            </button>
          </div>
        </div>
      </div>

      {/* Optimized Content */}
      {optimizedContent && (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Optimized Content</h3>
              <button
                onClick={handleCopy}
                className="flex items-center space-x-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                {copied ? <Check className="h-4 w-4" /> : <Copy className="h-4 w-4" />}
                <span>{copied ? 'Copied!' : 'Copy'}</span>
              </button>
            </div>
            
            <div className="bg-gray-50 rounded-lg p-4 border-l-4 border-blue-500">
              <pre className="whitespace-pre-wrap text-sm text-gray-800 font-medium">
                {optimizedContent}
              </pre>
            </div>
          </div>

          {/* Comparison */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                <Edit3 className="h-4 w-4 text-gray-600" />
                <span>Before</span>
              </h4>
              <div className="bg-red-50 rounded-lg p-4 border-l-4 border-red-300">
                <p className="text-sm text-gray-700 whitespace-pre-wrap">{currentContent}</p>
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <h4 className="font-semibold text-gray-900 mb-3 flex items-center space-x-2">
                <Sparkles className="h-4 w-4 text-green-600" />
                <span>After</span>
              </h4>
              <div className="bg-green-50 rounded-lg p-4 border-l-4 border-green-300">
                <p className="text-sm text-gray-700 whitespace-pre-wrap">{optimizedContent}</p>
              </div>
            </div>
          </div>

          {/* Optimization Tips */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h4 className="font-semibold text-gray-900 mb-3">Why This Works Better</h4>
            <div className="space-y-2 text-sm text-gray-700">
              {selectedSection === 'headline' && (
                <ul className="space-y-1">
                  <li>• Added relevant keywords for better searchability</li>
                  <li>• Included specific technologies and expertise</li>
                  <li>• Used action-oriented language</li>
                  <li>• Added emoji for visual appeal</li>
                </ul>
              )}
              {selectedSection === 'summary' && (
                <ul className="space-y-1">
                  <li>• Structured with clear sections and bullet points</li>
                  <li>• Included specific metrics and achievements</li>
                  <li>• Added relevant keywords for ATS optimization</li>
                  <li>• Ended with a clear call-to-action</li>
                </ul>
              )}
              {selectedSection === 'experience' && (
                <ul className="space-y-1">
                  <li>• Started each point with action verbs</li>
                  <li>• Included quantifiable results and metrics</li>
                  <li>• Highlighted collaboration and leadership</li>
                  <li>• Focused on impact and outcomes</li>
                </ul>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ContentOptimization;