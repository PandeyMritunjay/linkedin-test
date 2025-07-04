import React, { useState } from 'react';
import { Search, User, Award, TrendingUp, AlertCircle } from 'lucide-react';

const ProfileAnalysis: React.FC = () => {
  const [profileUrl, setProfileUrl] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    
    // Simulate API call with mock data
    setTimeout(() => {
      setAnalysisResult({
        overallScore: 78,
        sections: {
          headline: { score: 85, feedback: 'Strong headline with clear value proposition' },
          summary: { score: 72, feedback: 'Good summary but could be more specific about achievements' },
          experience: { score: 80, feedback: 'Well-detailed experience section' },
          skills: { score: 65, feedback: 'Add more relevant skills and get endorsements' },
          education: { score: 90, feedback: 'Complete education information' }
        },
        recommendations: [
          'Add 3-5 more relevant skills to your profile',
          'Include quantified achievements in your summary',
          'Get recommendations from colleagues',
          'Update your profile photo to a professional headshot'
        ],
        strengths: [
          'Clear professional headline',
          'Comprehensive work experience',
          'Strong educational background'
        ],
        improvements: [
          'Expand skills section',
          'Add more specific achievements',
          'Increase network connections'
        ]
      });
      setIsAnalyzing(false);
    }, 2000);
  };

  const handleDemoAnalysis = () => {
    setProfileUrl('https://linkedin.com/in/demo-profile');
    handleAnalyze();
  };

  return (
    <div className="space-y-6">
      {/* Input Section */}
      <div className="bg-white rounded-lg shadow-sm p-6">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">LinkedIn Profile Analysis</h2>
        <div className="flex space-x-4">
          <div className="flex-1">
            <input
              type="url"
              value={profileUrl}
              onChange={(e) => setProfileUrl(e.target.value)}
              placeholder="Enter LinkedIn profile URL (e.g., https://linkedin.com/in/username)"
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
            />
          </div>
          <button
            onClick={handleAnalyze}
            disabled={!profileUrl || isAnalyzing}
            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center space-x-2"
          >
            <Search className="h-4 w-4" />
            <span>{isAnalyzing ? 'Analyzing...' : 'Analyze'}</span>
          </button>
          <button
            onClick={handleDemoAnalysis}
            className="px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 flex items-center space-x-2"
          >
            <User className="h-4 w-4" />
            <span>Demo</span>
          </button>
        </div>
      </div>

      {/* Analysis Results */}
      {analysisResult && (
        <div className="space-y-6">
          {/* Overall Score */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-lg font-semibold text-gray-900">Overall Profile Score</h3>
              <div className="flex items-center space-x-2">
                <div className="text-3xl font-bold text-blue-600">{analysisResult.overallScore}</div>
                <div className="text-gray-500">/100</div>
              </div>
            </div>
            <div className="w-full bg-gray-200 rounded-full h-3">
              <div
                className="bg-blue-600 h-3 rounded-full transition-all duration-500"
                style={{ width: `${analysisResult.overallScore}%` }}
              ></div>
            </div>
          </div>

          {/* Section Scores */}
          <div className="bg-white rounded-lg shadow-sm p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Section Analysis</h3>
            <div className="space-y-4">
              {Object.entries(analysisResult.sections).map(([section, data]: [string, any]) => (
                <div key={section} className="border-l-4 border-blue-500 pl-4">
                  <div className="flex items-center justify-between mb-2">
                    <h4 className="font-medium text-gray-900 capitalize">{section}</h4>
                    <span className="text-sm font-semibold text-blue-600">{data.score}/100</span>
                  </div>
                  <p className="text-sm text-gray-600">{data.feedback}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Recommendations */}
          <div className="grid md:grid-cols-2 gap-6">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <TrendingUp className="h-5 w-5 text-green-600" />
                <h3 className="text-lg font-semibold text-gray-900">Strengths</h3>
              </div>
              <ul className="space-y-2">
                {analysisResult.strengths.map((strength: string, index: number) => (
                  <li key={index} className="flex items-start space-x-2">
                    <Award className="h-4 w-4 text-green-600 mt-0.5 flex-shrink-0" />
                    <span className="text-sm text-gray-700">{strength}</span>
                  </li>
                ))}
              </ul>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center space-x-2 mb-4">
                <AlertCircle className="h-5 w-5 text-orange-600" />
                <h3 className="text-lg font-semibold text-gray-900">Recommendations</h3>
              </div>
              <ul className="space-y-2">
                {analysisResult.recommendations.map((rec: string, index: number) => (
                  <li key={index} className="flex items-start space-x-2">
                    <div className="h-2 w-2 bg-orange-600 rounded-full mt-2 flex-shrink-0"></div>
                    <span className="text-sm text-gray-700">{rec}</span>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default ProfileAnalysis;