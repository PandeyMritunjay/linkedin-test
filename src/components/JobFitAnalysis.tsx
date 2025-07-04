import React, { useState } from 'react';
import { Target, TrendingUp, AlertTriangle, CheckCircle } from 'lucide-react';

const JobFitAnalysis: React.FC = () => {
  const [jobDescription, setJobDescription] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [fitResult, setFitResult] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!jobDescription.trim()) return;
    
    setIsAnalyzing(true);
    
    // Simulate API call with mock data
    setTimeout(() => {
      setFitResult({
        compatibilityScore: 82,
        matchedSkills: [
          'JavaScript', 'React', 'Node.js', 'Python', 'SQL', 'Git'
        ],
        missingSkills: [
          'Docker', 'Kubernetes', 'AWS', 'GraphQL'
        ],
        strengths: [
          'Strong frontend development experience',
          'Proven track record in full-stack development',
          'Experience with modern JavaScript frameworks'
        ],
        gaps: [
          'Limited cloud platform experience',
          'No containerization experience mentioned',
          'GraphQL knowledge would be beneficial'
        ],
        recommendations: [
          'Highlight your React and Node.js experience prominently',
          'Consider taking an AWS certification course',
          'Build a project using Docker to demonstrate containerization skills',
          'Learn GraphQL basics through online tutorials'
        ]
      });
      setIsAnalyzing(false);
    }, 2000);
  };

  const sampleJobDescription = `Senior Full Stack Developer

We are looking for an experienced Full Stack Developer to join our team. The ideal candidate will have:

Required Skills:
- 5+ years of experience in JavaScript/TypeScript
- Proficiency in React and Node.js
- Experience with SQL databases
- Knowledge of RESTful APIs
- Git version control

Preferred Skills:
- AWS cloud services
- Docker and Kubernetes
- GraphQL
- CI/CD pipelines
- Agile development methodologies

Responsibilities:
- Develop and maintain web applications
- Collaborate with cross-functional teams
- Write clean, maintainable code
- Participate in code reviews`;

  const handleUseSample = () => {
    setJobDescription(sampleJobDescription);
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Job Fit Analysis</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Job Description
            </label>
            <textarea
              value={jobDescription}
              onChange={(e) => setJobDescription(e.target.value)}
              placeholder="Paste the job description here..."
              rows={8}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <div className="flex space-x-4">
            <button
              onClick={handleAnalyze}
              disabled={!jobDescription.trim() || isAnalyzing}
              className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
            >
              <Target className="h-4 w-4" />
              <span>{isAnalyzing ? 'Analyzing...' : 'Analyze Fit'}</span>
            </button>
            <button
              onClick={handleUseSample}
              className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200"
            >
              Use Sample Job
            </button>
          </div>
        </div>
      </div>

      {/* Analysis Results */}
      {fitResult && (
        <div className="space-y-6">
          {/* Compatibility Score */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Job Compatibility Score</h3>
              <div className="flex items-center space-x-2">
                <div className="text-3xl font-bold text-green-600">{fitResult.compatibilityScore}</div>
                <div className="text-gray-500">/100</div>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-green-600 h-3 rounded-full transition-all duration-500"
                style={{ width: `${fitResult.compatibilityScore}%` }}
              ></div>
            </div>
            <p className="text-sm text-gray-600 mt-2">
              {fitResult.compatibilityScore >= 80 ? 'Excellent match!' : 
               fitResult.compatibilityScore >= 60 ? 'Good match with some gaps to address' : 
               'Consider developing missing skills before applying'}
            </p>
          </div>

          {/* Skills Analysis */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <CheckCircle className="h-5 w-5 text-green-600" />
                <h3 className="text-lg font-semibold text-gray-900">Matched Skills</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {fitResult.matchedSkills.map((skill: string, index: number) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <AlertTriangle className="h-5 w-5 text-orange-600" />
                <h3 className="text-lg font-semibold text-gray-900">Missing Skills</h3>
              </div>
              <div className="flex flex-wrap gap-2">
                {fitResult.missingSkills.map((skill: string, index: number) => (
                  <span
                    key={index}
                    className="px-3 py-1 bg-orange-100 text-orange-800 rounded-full text-sm font-medium"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Detailed Analysis */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <TrendingUp className="h-5 w-5 text-blue-600" />
                <h3 className="text-lg font-semibold text-gray-900">Your Strengths</h3>
              </div>
              <ul className="space-y-2">
                {fitResult.strengths.map((strength: string, index: number) => (
                  <li key={index} className="flex items-start space-x-2">
                    <CheckCircle className="h-4 w-4 text-blue-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <AlertTriangle className="h-5 w-5 text-red-600" />
                <h3 className="text-lg font-semibold text-gray-900">Areas to Improve</h3>
              </div>
              <ul className="space-y-2">
                {fitResult.gaps.map((gap: string, index: number) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="h-2 w-2 bg-red-600 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-sm text-gray-700">{gap}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>

          {/* Recommendations */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Action Plan</h3>
            <div className="space-y-3">
              {fitResult.recommendations.map((rec: string, index: number) => (
                <div key={index} className="flex items-start space-x-3 p-3 bg-blue-50 rounded-lg">
                  <div className="flex-shrink-0 w-6 h-6 bg-blue-600 text-white rounded-full flex items-center justify-center text-sm font-medium">
                    {index + 1}
                  </div>
                  <span className="text-sm text-gray-700">{rec}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default JobFitAnalysis;