/**
 * CashCommanderResults component for displaying cash forecast analysis
 * with professional financial dashboard visualization.
 */
import React, { useState } from 'react';
import { formatCurrency, formatNumber, parseMarkdownTable } from '@/utils/format';
import Button from '@/components/common/Button';

interface CashCommanderResultsProps {
  output: {
    current_cash_position?: number;
    forecast?: any[];
    recommendations?: string[];
    liquidity_warnings?: string[];
    summary?: string;
  };
  workOrderId: number;
  onDownloadExcel?: () => void;
}

/**
 * Display Cash Commander analysis results with KPI cards,
 * forecast table, and actionable insights.
 */
const CashCommanderResults: React.FC<CashCommanderResultsProps> = ({
  output,
  workOrderId,
  onDownloadExcel,
}) => {
  const [showFullTable, setShowFullTable] = useState(false);

  // Parse forecast data from markdown table in summary
  const forecastRows = output.summary
    ? parseMarkdownTable(output.summary)
    : [];

  // Extract metrics from the summary or output
  const currentCash = output.current_cash_position || 0;

  // Calculate weekly collection rate from forecast data
  const weeklyReceipts = forecastRows.length > 0 && forecastRows[0].Receipts
    ? parseFloat(forecastRows[0].Receipts.replace(/[$,]/g, ''))
    : 0;

  const weeklyDisbursements = forecastRows.length > 0 && forecastRows[0].Disbursements
    ? parseFloat(forecastRows[0].Disbursements.replace(/[$,]/g, ''))
    : 0;

  const netCashFlow = weeklyReceipts - weeklyDisbursements;

  // Determine if there are any warnings
  const hasWarnings = output.liquidity_warnings && output.liquidity_warnings.length > 0;
  const hasRecommendations = output.recommendations && output.recommendations.length > 0;

  return (
    <div className="space-y-6">
      {/* KPI Cards - Hero Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Current Cash Position */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="text-xs text-gray-600 uppercase tracking-wide mb-2">
            Current Cash Position
          </div>
          <div className="text-3xl font-bold text-gray-900 mt-2">
            {formatCurrency(currentCash, 0)}
          </div>
          <div className="text-sm text-gray-500 mt-3">
            As of {new Date().toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
          </div>
        </div>

        {/* Weekly Net Cash Flow */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="text-xs text-gray-600 uppercase tracking-wide mb-2">
            Weekly Net Cash Flow
          </div>
          <div className={`text-3xl font-bold mt-2 ${netCashFlow >= 0 ? 'text-green-600' : 'text-red-600'}`}>
            {netCashFlow >= 0 ? '+' : ''}{formatCurrency(netCashFlow, 0)}
          </div>
          <div className="text-sm text-gray-500 mt-3">
            Receipts {formatCurrency(weeklyReceipts, 0)} • Disbursements {formatCurrency(weeklyDisbursements, 0)}
          </div>
        </div>

        {/* Forecast Horizon */}
        <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-200">
          <div className="text-xs text-gray-600 uppercase tracking-wide mb-2">
            Forecast Horizon
          </div>
          <div className="text-5xl font-bold text-blue-600 mt-2">
            13
          </div>
          <div className="text-sm text-gray-500 mt-3">
            Weeks • {forecastRows.length} periods analyzed
          </div>
        </div>
      </div>

      {/* Liquidity Warnings (if any) */}
      {hasWarnings && (
        <div className="bg-red-50 border-l-4 border-red-400 rounded-lg p-6">
          <div className="flex items-start">
            <svg
              className="w-6 h-6 text-red-400 flex-shrink-0 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z"
                clipRule="evenodd"
              />
            </svg>
            <div className="ml-4 flex-1">
              <h4 className="text-sm font-semibold text-red-900 mb-3">
                ⚠️ Liquidity Warnings
              </h4>
              <div className="space-y-2">
                {output.liquidity_warnings?.map((warning, idx) => (
                  <div key={idx} className="text-sm text-red-800 leading-relaxed">
                    • {warning}
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 13-Week Forecast Table */}
      {forecastRows.length > 0 && (
        <div className="bg-white rounded-lg shadow-sm border border-gray-200">
          <div className="px-6 py-4 border-b border-gray-200 flex items-center justify-between">
            <h3 className="text-lg font-semibold text-gray-900">
              13-Week Rolling Cash Forecast
            </h3>
            {forecastRows.length > 5 && (
              <button
                onClick={() => setShowFullTable(!showFullTable)}
                className="text-sm text-blue-600 hover:text-blue-800 font-medium"
              >
                {showFullTable ? 'Show Less' : 'Show All Weeks'}
              </button>
            )}
          </div>
          <div className="overflow-x-auto">
            <table className="min-w-full divide-y divide-gray-200">
              <thead className="bg-gray-50">
                <tr>
                  <th className="px-6 py-3 text-left text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Week
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Beginning Balance
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Receipts
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Disbursements
                  </th>
                  <th className="px-6 py-3 text-right text-xs font-semibold text-gray-700 uppercase tracking-wider">
                    Ending Balance
                  </th>
                </tr>
              </thead>
              <tbody className="bg-white divide-y divide-gray-200">
                {(showFullTable ? forecastRows : forecastRows.slice(0, 5)).map((row, idx) => (
                  <tr key={idx} className={idx % 2 === 0 ? 'bg-white' : 'bg-gray-50'}>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900">
                      {row.Week}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-gray-900">
                      {row['Beginning Balance'] || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-green-600 font-medium">
                      {row.Receipts || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right text-red-600 font-medium">
                      {row.Disbursements || '—'}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-right font-semibold text-gray-900">
                      {row['Ending Balance'] || '—'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* Recommendations */}
      {hasRecommendations && (
        <div className="bg-blue-50 border-l-4 border-blue-400 rounded-lg p-6">
          <div className="flex items-start">
            <svg
              className="w-6 h-6 text-blue-400 flex-shrink-0 mt-0.5"
              fill="currentColor"
              viewBox="0 0 20 20"
            >
              <path
                fillRule="evenodd"
                d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z"
                clipRule="evenodd"
              />
            </svg>
            <div className="ml-4 flex-1">
              <h4 className="text-sm font-semibold text-blue-900 mb-3">
                💡 Recommendations
              </h4>
              <div className="space-y-2">
                {output.recommendations?.map((rec, idx) => (
                  <div key={idx} className="flex items-start text-sm text-blue-800 leading-relaxed">
                    <svg
                      className="w-5 h-5 mr-2 flex-shrink-0 text-blue-600 mt-0.5"
                      fill="currentColor"
                      viewBox="0 0 20 20"
                    >
                      <path
                        fillRule="evenodd"
                        d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                        clipRule="evenodd"
                      />
                    </svg>
                    <span>{rec}</span>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Download Excel Button */}
      <div className="flex items-center justify-between bg-gray-50 rounded-lg p-6 border border-gray-200">
        <div className="flex items-start">
          <svg
            className="w-10 h-10 text-green-600 mr-4"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path
              fillRule="evenodd"
              d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z"
              clipRule="evenodd"
            />
          </svg>
          <div>
            <h4 className="text-base font-semibold text-gray-900">
              Cash Ladder Excel Report
            </h4>
            <p className="text-sm text-gray-600 mt-1">
              Download the complete 13-week cash forecast with detailed calculations,
              assumptions, and recommendations in Excel format.
            </p>
          </div>
        </div>
        <Button
          variant="primary"
          onClick={onDownloadExcel}
          className="ml-6 flex-shrink-0"
        >
          <svg
            className="w-5 h-5 mr-2"
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"
            />
          </svg>
          Download Excel
        </Button>
      </div>
    </div>
  );
};

export default CashCommanderResults;
