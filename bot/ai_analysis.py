"""
AI Analysis module using local Mistral LLM for expense analysis.
Implements a flow-based approach for processing data in stages.
"""
import json
import logging
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
import ollama
from sheets.operations import SheetOperations

logger = logging.getLogger(__name__)

@dataclass
class ExpenseCategory:
    """Represents a categorized expense group."""
    name: str
    total_amount: float
    count: int
    descriptions: List[str]
    patterns: List[str]

@dataclass
class AnalysisResult:
    """Represents the complete analysis result."""
    period: str
    total_expenses: float
    total_transactions: int
    categories: List[ExpenseCategory]
    insights: List[str]
    recommendations: List[str]
    analysis_date: str

class MistralAnalyzer:
    """AI-powered expense analyzer using local Mistral LLM."""
    
    def __init__(self, model_name: str = "mistral"):
        """Initialize the Mistral analyzer."""
        self.model_name = model_name
        self.sheet_ops = SheetOperations()
        self.client = ollama.Client()
        
        # Ensure the model is available
        try:
            self._ensure_model_available()
        except Exception as e:
            logger.error(f"Failed to ensure model availability: {e}")
    
    def _ensure_model_available(self):
        """Ensure the Mistral model is available locally."""
        try:
            models = self.client.list()
            if not any(model['name'] == self.model_name for model in models['models']):
                logger.info(f"Pulling {self.model_name} model...")
                self.client.pull(self.model_name)
                logger.info(f"Successfully pulled {self.model_name} model")
        except Exception as e:
            logger.error(f"Error ensuring model availability: {e}")
            raise
    
    def _extract_expense_data(self, period: str) -> pd.DataFrame:
        """
        Extract expense data from sheets for the specified period.
        
        Args:
            period: 'monthly' or 'annual'
            
        Returns:
            DataFrame with expense data
        """
        try:
            # Get expense data from SheetOperations
            success, message, expense_data = self.sheet_ops.get_expense_data_for_analysis(period)
            
            if not success:
                raise ValueError(f"Failed to get expense data: {message}")
            
            if not expense_data:
                # If no real data, create sample data for demonstration
                logger.warning(f"No expense data found for {period} period, using sample data")
                sample_data = self._create_sample_data(period)
                return sample_data
            
            # Convert to DataFrame
            df = pd.DataFrame(expense_data)
            
            # Ensure required columns exist
            if 'amount' not in df.columns or 'description' not in df.columns:
                logger.warning("Missing required columns, using sample data")
                sample_data = self._create_sample_data(period)
                return sample_data
            
            logger.info(f"Successfully extracted {len(df)} expenses for {period} analysis")
            return df
            
        except Exception as e:
            logger.error(f"Error extracting expense data: {e}")
            raise
    
    def _create_sample_data(self, period: str) -> pd.DataFrame:
        """Create sample data for demonstration purposes."""
        if period == 'monthly':
            # Sample monthly data
            data = {
                'date': ['2024-01-15', '2024-01-16', '2024-01-17', '2024-01-18', '2024-01-19'],
                'amount': [12.50, 8.75, 15.00, 22.50, 9.99],
                'description': ['matcha latte', 'coffee', 'matcha latte', 'lunch', 'matcha latte'],
                'category': ['Food', 'Food', 'Food', 'Food', 'Food']
            }
        else:  # annual
            # Sample annual data with more variety
            data = {
                'date': ['2024-01-15', '2024-02-20', '2024-03-10', '2024-04-05', '2024-05-12'],
                'amount': [12.50, 45.00, 8.75, 120.00, 15.00],
                'description': ['matcha latte', 'gas', 'coffee', 'shopping', 'matcha latte'],
                'category': ['Food', 'Transportation', 'Food', 'Shopping', 'Food']
            }
        
        return pd.DataFrame(data)
    
    def _categorize_expenses_flow(self, expenses_df: pd.DataFrame) -> List[ExpenseCategory]:
        """
        Flow 1: Categorize expenses using AI prompts.
        This is the first stage of analysis.
        """
        try:
            # Prepare data for categorization
            descriptions = expenses_df['description'].tolist()
            amounts = expenses_df['amount'].tolist()
            
            # Create the categorization prompt
            prompt = self._create_categorization_prompt(descriptions, amounts)
            
            # Get AI response
            response = self._get_ai_response(prompt)
            
            # Parse the categorized response
            categories = self._parse_categorization_response(response)
            
            return categories
            
        except Exception as e:
            logger.error(f"Error in categorization flow: {e}")
            raise
    
    def _analyze_patterns_flow(self, categories: List[ExpenseCategory]) -> List[ExpenseCategory]:
        """
        Flow 2: Analyze spending patterns within categories.
        This is the second stage of analysis.
        """
        try:
            for category in categories:
                if category.count > 1:
                    # Analyze patterns for categories with multiple transactions
                    pattern_prompt = self._create_pattern_analysis_prompt(category)
                    pattern_response = self._get_ai_response(pattern_prompt)
                    
                    # Extract patterns from response
                    patterns = self._extract_patterns_from_response(pattern_response)
                    category.patterns = patterns
            
            return categories
            
        except Exception as e:
            logger.error(f"Error in pattern analysis flow: {e}")
            raise
    
    def _generate_insights_flow(self, categories: List[ExpenseCategory], 
                               total_amount: float, total_count: int) -> List[str]:
        """
        Flow 3: Generate insights and recommendations.
        This is the final stage of analysis.
        """
        try:
            insights_prompt = self._create_insights_prompt(
                categories, total_amount, total_count
            )
            
            insights_response = self._get_ai_response(insights_prompt)
            
            # Parse insights and recommendations
            insights, recommendations = self._parse_insights_response(insights_response)
            
            return insights, recommendations
            
        except Exception as e:
            logger.error(f"Error in insights generation flow: {e}")
            raise
    
    def _create_categorization_prompt(self, descriptions: List[str], amounts: List[float]) -> str:
        """Create the prompt for expense categorization."""
        prompt = f"""
You are an expert financial analyst. Analyze the following expenses and categorize them into logical groups.

Expense Data:
{chr(10).join([f"${amount:.2f} - {desc}" for amount, desc in zip(amounts, descriptions)])}

Instructions:
1. Group similar expenses into categories (e.g., Food, Transportation, Entertainment, etc.)
2. Look for common themes in descriptions
3. Consider amounts when grouping
4. Return your response in this exact JSON format:

{{
    "categories": [
        {{
            "name": "Category Name",
            "total_amount": 0.00,
            "count": 0,
            "descriptions": ["desc1", "desc2"],
            "patterns": []
        }}
    ]
}}

Be specific with category names and ensure all expenses are categorized.
"""
        return prompt
    
    def _create_pattern_analysis_prompt(self, category: ExpenseCategory) -> str:
        """Create the prompt for pattern analysis within a category."""
        prompt = f"""
Analyze the spending patterns in the "{category.name}" category.

Category: {category.name}
Total Amount: ${category.total_amount:.2f}
Transaction Count: {category.count}
Descriptions: {', '.join(category.descriptions)}

Instructions:
1. Identify recurring patterns (e.g., "matcha 20 times")
2. Look for frequency patterns
3. Identify spending habits
4. Return your response in this exact JSON format:

{{
    "patterns": [
        "Pattern description 1",
        "Pattern description 2"
    ]
}}

Focus on actionable insights about spending behavior.
"""
        return prompt
    
    def _create_insights_prompt(self, categories: List[ExpenseCategory], 
                                total_amount: float, total_count: int) -> str:
        """Create the prompt for generating insights and recommendations."""
        prompt = f"""
Generate financial insights and recommendations based on this expense analysis.

Summary:
- Total Expenses: ${total_amount:.2f}
- Total Transactions: {total_count}
- Categories: {len(categories)}

Category Breakdown:
{chr(10).join([f"- {cat.name}: ${cat.total_amount:.2f} ({cat.count} transactions)" for cat in categories])}

Instructions:
1. Identify key spending patterns
2. Highlight areas of concern
3. Provide actionable recommendations
4. Return your response in this exact JSON format:

{{
    "insights": [
        "Insight 1",
        "Insight 2"
    ],
    "recommendations": [
        "Recommendation 1",
        "Recommendation 2"
    ]
}}

Be specific and actionable with your insights.
"""
        return prompt
    
    def _get_ai_response(self, prompt: str) -> str:
        """Get response from the local Mistral LLM."""
        try:
            response = self.client.chat(
                model=self.model_name,
                messages=[{
                    'role': 'user',
                    'content': prompt
                }]
            )
            return response['message']['content']
        except Exception as e:
            logger.error(f"Error getting AI response: {e}")
            raise
    
    def _parse_categorization_response(self, response: str) -> List[ExpenseCategory]:
        """Parse the AI response for expense categorization."""
        try:
            # Extract JSON from response
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                raise ValueError("No JSON found in response")
            
            json_str = response[json_start:json_end]
            data = json.loads(json_str)
            
            categories = []
            for cat_data in data.get('categories', []):
                category = ExpenseCategory(
                    name=cat_data.get('name', 'Unknown'),
                    total_amount=float(cat_data.get('total_amount', 0)),
                    count=int(cat_data.get('count', 0)),
                    descriptions=cat_data.get('descriptions', []),
                    patterns=cat_data.get('patterns', [])
                )
                categories.append(category)
            
            return categories
            
        except Exception as e:
            logger.error(f"Error parsing categorization response: {e}")
            raise
    
    def _extract_patterns_from_response(self, response: str) -> List[str]:
        """Extract patterns from the AI response."""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return []
            
            json_str = response[json_start:json_end]
            data = json.loads(json_str)
            
            return data.get('patterns', [])
            
        except Exception as e:
            logger.error(f"Error extracting patterns: {e}")
            return []
    
    def _parse_insights_response(self, response: str) -> Tuple[List[str], List[str]]:
        """Parse insights and recommendations from the AI response."""
        try:
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            
            if json_start == -1 or json_end == 0:
                return [], []
            
            json_str = response[json_start:json_end]
            data = json.loads(json_str)
            
            insights = data.get('insights', [])
            recommendations = data.get('recommendations', [])
            
            return insights, recommendations
            
        except Exception as e:
            logger.error(f"Error parsing insights response: {e}")
            return [], []
    
    def analyze_expenses(self, period: str = 'monthly') -> AnalysisResult:
        """
        Perform complete expense analysis using the flow-based approach.
        
        Args:
            period: 'monthly' or 'annual'
            
        Returns:
            AnalysisResult with complete analysis
        """
        try:
            logger.info(f"Starting {period} expense analysis...")
            
            # Extract expense data
            expenses_df = self._extract_expense_data(period)
            
            if expenses_df.empty:
                raise ValueError(f"No expense data found for {period} period")
            
            # Flow 1: Categorize expenses
            logger.info("Flow 1: Categorizing expenses...")
            categories = self._categorize_expenses_flow(expenses_df)
            
            # Flow 2: Analyze patterns
            logger.info("Flow 2: Analyzing patterns...")
            categories = self._analyze_patterns_flow(categories)
            
            # Calculate totals
            total_amount = sum(cat.total_amount for cat in categories)
            total_count = sum(cat.count for cat in categories)
            
            # Flow 3: Generate insights
            logger.info("Flow 3: Generating insights...")
            insights, recommendations = self._generate_insights_flow(
                categories, total_amount, total_count
            )
            
            # Create analysis result
            result = AnalysisResult(
                period=period,
                total_expenses=total_amount,
                total_transactions=total_count,
                categories=categories,
                insights=insights,
                recommendations=recommendations,
                analysis_date=datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            )
            
            logger.info(f"Completed {period} analysis successfully")
            return result
            
        except Exception as e:
            logger.error(f"Error in expense analysis: {e}")
            raise
    
    def format_analysis_report(self, result: AnalysisResult) -> str:
        """Format the analysis result into a readable report."""
        try:
            report = f"🤖 **AI Expense Analysis Report**\n\n"
            report += f"📅 **Period**: {result.period.title()}\n"
            report += f"📊 **Total Expenses**: ${result.total_expenses:.2f}\n"
            report += f"🔢 **Total Transactions**: {result.total_transactions}\n"
            report += f"📅 **Analysis Date**: {result.analysis_date}\n\n"
            
            # Category breakdown
            report += "📂 **Category Breakdown**\n"
            for category in result.categories:
                report += f"• **{category.name}**: ${category.total_amount:.2f} ({category.count} transactions)\n"
                
                # Show patterns if any
                if category.patterns:
                    for pattern in category.patterns:
                        report += f"  - {pattern}\n"
                report += "\n"
            
            # Insights
            if result.insights:
                report += "💡 **Key Insights**\n"
                for insight in result.insights:
                    report += f"• {insight}\n"
                report += "\n"
            
            # Recommendations
            if result.recommendations:
                report += "🎯 **Recommendations**\n"
                for rec in result.recommendations:
                    report += f"• {rec}\n"
                report += "\n"
            
            return report
            
        except Exception as e:
            logger.error(f"Error formatting analysis report: {e}")
            raise
