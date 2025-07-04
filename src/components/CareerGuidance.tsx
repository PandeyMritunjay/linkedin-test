import React, { useState } from 'react';
import { Target, TrendingUp, BookOpen, Users, Calendar, Star } from 'lucide-react';

const CareerGuidance: React.FC = () => {
  const [careerGoals, setCareerGoals] = useState('');
  const [currentRole, setCurrentRole] = useState('');
  const [experience, setExperience] = useState('');
  const [isGenerating, setIsGenerating] = useState(false);
  const [guidance, setGuidance] = useState<any>(null);

  const handleGenerate = async () => {
    if (!careerGoals.trim()) return;
    
    setIsGenerating(true);
    
    // Simulate API call with mock guidance data
    setTimeout(() => {
      setGuidance({
        roadmap: [
          {
            phase: 'Short-term (3-6 months)',
            goals: [
              'Complete AWS Cloud Practitioner certification',
              'Build 2-3 projects showcasing full-stack skills',
              'Contribute to 1-2 open source projects',
              'Expand professional network by 50+ connections'
            ]
          },
          {
            phase: 'Medium-term (6-12 months)',
            goals: [
              'Obtain AWS Solutions Architect Associate certification',
              'Lead a team project or initiative',
              'Speak at a local tech meetup or conference',
              'Mentor 1-2 junior developers'
            ]
          },
          {
            phase: 'Long-term (1-2 years)',
            goals: [
              'Transition to Senior/Lead Developer role',
              'Develop expertise in system architecture',
              'Build a strong personal brand in tech',
              'Consider starting a tech blog or YouTube channel'
            ]
          }
        ],
        skillPriorities: [
          { skill: 'Cloud Architecture (AWS/Azure)', priority: 'High', reason: 'Essential for senior roles' },
          { skill: 'System Design', priority: 'High', reason: 'Critical for leadership positions' },
          { skill: 'Team Leadership', priority: 'Medium', reason: 'Important for career progression' },
          { skill: 'DevOps/CI-CD', priority: 'Medium', reason: 'Valuable for full-stack expertise' },
          { skill: 'Data Structures & Algorithms', priority: 'Low', reason: 'Good for interview prep' }
        ],
        learningResources: [
          { title: 'AWS Certified Solutions Architect Course', type: 'Course', platform: 'A Cloud Guru' },
          { title: 'System Design Interview', type: 'Book', platform: 'Amazon' },
          { title: 'The Manager\'s Path', type: 'Book', platform: 'O\'Reilly' },
          { title: 'Docker & Kubernetes Course', type: 'Course', platform: 'Udemy' }
        ],
        networkingTips: [
          'Join local tech meetups and developer communities',
          'Engage actively on LinkedIn with industry content',
          'Attend virtual conferences and webinars',
          'Connect with professionals in your target companies',
          'Participate in hackathons and coding challenges'
        ],
        nextSteps: [
          'Update LinkedIn profile with career objectives',
          'Start working on AWS certification immediately',
          'Identify 3-5 target companies for future applications',
          'Schedule informational interviews with senior developers',
          'Create a learning schedule and stick to it'
        ]
      });
      setIsGenerating(false);
    }, 2500);
  };

  const handleUseSample = () => {
    setCareerGoals('I want to become a Senior Full Stack Developer and eventually move into a technical leadership role');
    setCurrentRole('Full Stack Developer');
    setExperience('3 years');
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Career Guidance & Development Plan</h2>
        
        <div className="space-y-4">
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Current Role
              </label>
              <input
                type="text"
                value={currentRole}
                onChange={(e) => setCurrentRole(e.target.value)}
                placeholder="e.g., Software Developer, Product Manager"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Years of Experience
              </label>
              <select
                value={experience}
                onChange={(e) => setExperience(e.target.value)}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              >
                <option value="">Select experience</option>
                <option value="0-1">0-1 years</option>
                <option value="2-3">2-3 years</option>
                <option value="4-5">4-5 years</option>
                <option value="6-10">6-10 years</option>
                <option value="10+">10+ years</option>
              </select>
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Career Goals & Aspirations
            </label>
            <textarea
              value={careerGoals}
              onChange={(e) => setCareerGoals(e.target.value)}
              placeholder="Describe your career goals, target roles, and what you want to achieve..."
              rows={4}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>

          <div className="flex space-x-4">
            <button
              onClick={handleGenerate}
              disabled={!careerGoals.trim() || isGenerating}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <Target className="h-4 w-4" />
              <span>{isGenerating ? 'Generating Plan...' : 'Generate Career Plan'}</span>
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

      {/* Career Guidance Results */}
      {guidance && (
        <div className="space-y-6">
          {/* Career Roadmap */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center space-x-2 mb-4">
              <Calendar className="h-5 w-5 text-blue-600" />
              <h3 className="text-lg font-semibold text-gray-900">Career Roadmap</h3>
            </div>
            <div className="space-y-6">
              {guidance.roadmap.map((phase: any, index: number) => (
                <div key={index} className="relative">
                  <div className="flex items-center space-x-3 mb-3">
                    <div className="flex-shrink-0 w-8 h-8 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                      {index + 1}
                    </div>
                    <h4 className="font-semibold text-gray-900">{phase.phase}</h4>
                  </div>
                  <div className="ml-11 space-y-2">
                    {phase.goals.map((goal: string, goalIndex: number) => (
                      <div key={goalIndex} className="flex items-start space-x-2">
                        <div className="h-2 w-2 bg-blue-400 rounded-full mt-2 flex-shrink-0"></div>
                        <span className="text-sm text-gray-700">{goal}</span>
                      </div>
                    ))}
                  </div>
                  {index < guidance.roadmap.length - 1 && (
                    <div className="absolute left-4 top-12 w-0.5 h-8 bg-gray-300"></div>
                  )}
                </div>
              ))}
            </div>
          </div>

          {/* Skill Priorities */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center space-x-2 mb-4">
              <TrendingUp className="h-5 w-5 text-green-600" />
              <h3 className="text-lg font-semibold text-gray-900">Skill Development Priorities</h3>
            </div>
            <div className="space-y-3">
              {guidance.skillPriorities.map((item: any, index: number) => (
                <div key={index} className="flex items-center justify-between p-3 bg-gray-50 rounded-lg">
                  <div className="flex-1">
                    <h4 className="font-medium text-gray-900">{item.skill}</h4>
                    <p className="text-sm text-gray-600">{item.reason}</p>
                  </div>
                  <span className={`px-3 py-1 rounded-full text-xs font-medium ${
                    item.priority === 'High' ? 'bg-red-100 text-red-800' :
                    item.priority === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                    'bg-green-100 text-green-800'
                  }`}>
                    {item.priority}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Learning Resources */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center space-x-2 mb-4">
              <BookOpen className="h-5 w-5 text-purple-600" />
              <h3 className="text-lg font-semibold text-gray-900">Recommended Learning Resources</h3>
            </div>
            <div className="grid md:grid-cols-2 gap-4">
              {guidance.learningResources.map((resource: any, index: number) => (
                <div key={index} className="border border-gray-200 rounded-lg p-4">
                  <div className="flex items-start space-x-3">
                    <div className={`p-2 rounded-lg ${
                      resource.type === 'Course' ? 'bg-blue-100' : 'bg-green-100'
                    }`}>
                      {resource.type === 'Course' ? 
                        <BookOpen className="h-4 w-4 text-blue-600" /> :
                        <Star className="h-4 w-4 text-green-600" />
                      }
                    </div>
                    <div className="flex-1">
                      <h4 className="font-medium text-gray-900">{resource.title}</h4>
                      <p className="text-sm text-gray-600">{resource.platform}</p>
                      <span className="inline-block mt-1 px-2 py-1 bg-gray-100 text-gray-700 rounded text-xs">
                        {resource.type}
                      </span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Networking & Next Steps */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Users className="h-5 w-5 text-orange-600" />
                <h3 className="text-lg font-semibold text-gray-900">Networking Strategy</h3>
              </div>
              <ul className="space-y-2">
                {guidance.networkingTips.map((tip: string, index: number) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="h-2 w-2 bg-orange-600 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-sm text-gray-700">{tip}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <Target className="h-5 w-5 text-red-600" />
                <h3 className="text-lg font-semibold text-gray-900">Immediate Next Steps</h3>
              </div>
              <div className="space-y-3">
                {guidance.nextSteps.map((step: string, index: number) => (
                  <div key={index} className="flex items-start space-x-3 p-2 bg-red-50 rounded-lg">
                    <div className="flex-shrink-0 w-6 h-6 bg-red-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                      {index + 1}
                    </div>
                    <span className="text-sm text-gray-700">{step}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default CareerGuidance;