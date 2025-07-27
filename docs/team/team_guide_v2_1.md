# 👥 Ash Analytics Dashboard Team Guide

User-focused guide for Crisis Response teams using ash-dash v2.1

---

## 🌟 Welcome to Your Dashboard

The Ash Analytics Dashboard is your central hub for monitoring the mental health crisis detection system serving [The Alphabet Cartel](https://discord.gg/alphabetcartel) Discord community. This guide will help you understand, navigate, and effectively use the dashboard to support your community's wellbeing.

### **What You Can Do**

- **Monitor Crisis Detection**: Track how well the system is identifying and responding to mental health concerns
- **View Learning Progress**: See how the AI system improves based on your team's feedback
- **Check Service Health**: Ensure all components are running smoothly
- **Access Testing Results**: Review comprehensive testing data and performance metrics
- **Export Data**: Generate reports for analysis and record-keeping
- **Manage Team Access**: Control who can view what information (admin roles)

---

## 🚀 Getting Started

### **Accessing the Dashboard**

**Primary URL**: https://10.20.30.16:8883

**What You'll Need:**
- Modern web browser (Chrome, Firefox, Edge, Safari)
- Network access to the server (usually automatic within your organization)
- Team member account (contact your administrator if needed)

**First Login:**
1. Navigate to https://10.20.30.16:8883
2. You may see a security warning about certificates - this is normal for internal tools
3. Click "Advanced" → "Proceed to site" (exact wording varies by browser)
4. The dashboard will load automatically

### **Dashboard Layout**

**Header Section:**
- Service status indicators (green = good, red = issues)
- Last update timestamp
- Quick navigation menu

**Main Content:**
- Crisis detection metrics and trends
- Learning system progress
- Testing suite results
- Interactive charts and graphs

**Footer:**
- Links to documentation
- Team contact information
- System version information

---

## 📊 Understanding the Dashboard

### **Service Status Row**

The top of your dashboard shows the health of all system components:

#### **🤖 Ash Bot Status**
- **Green**: Bot is online and responding to crisis situations
- **Yellow**: Bot is experiencing some delays but still functional
- **Red**: Bot is offline or having serious issues - immediate attention needed

*What this means*: This is your Discord bot that actually detects and responds to crisis situations in chat.

#### **🧠 NLP Server Status**  
- **Green**: AI analysis system is working normally
- **Yellow**: Some performance issues but still analyzing messages
- **Red**: AI system is down - detection accuracy may be reduced

*What this means*: This is the "brain" that uses machine learning to understand crisis language.

#### **🧪 Testing Suite Status**
- **Green**: Automated testing is running and passing
- **Yellow**: Some tests failing but core functionality works
- **Red**: Major testing failures - system reliability uncertain

*What this means*: This continuously tests the system to ensure it's working correctly.

#### **📊 Dashboard Status**
- **Green**: This dashboard is working normally  
- **Yellow**: Some features may be slow or unavailable
- **Red**: Dashboard is having problems - refresh the page

*What this means*: The health of this monitoring system itself.

### **Crisis Detection Metrics**

These numbers show how the system is performing at its core mission:

#### **Crisis Level Breakdown (Last 24 Hours)**
- **🔴 High Crisis (X alerts)**: Immediate intervention situations detected
- **🟡 Medium Crisis (X alerts)**: Concerning situations requiring monitoring
- **🟢 Low Crisis (X alerts)**: Mild concerns with gentle support offered
- **📝 Total Messages (X analyzed)**: All messages the system reviewed

#### **What These Numbers Mean**
- **Higher numbers aren't necessarily bad** - they might indicate the system is correctly identifying situations that need attention
- **Sudden spikes** might indicate a community crisis or system sensitivity changes
- **Zero detections for extended periods** might indicate the system isn't working properly

#### **Detection Accuracy**
- **False Positive Rate**: Percentage of alerts that weren't actually crises
- **False Negative Rate**: Percentage of missed crises (based on team corrections)
- **Overall Accuracy**: How often the system gets it right

### **Learning System Analytics**

This section shows how the AI system improves over time:

#### **Learning Effectiveness**
- **Community Adaptations**: How many times the system learned from your team's feedback
- **Pattern Recognition**: New crisis language patterns the system discovered
- **Accuracy Improvements**: Percentage improvement in detection over time

#### **Team Corrections Tracking**
- **False Positive Corrections**: Times your team reported "this wasn't a crisis"
- **False Negative Corrections**: Times your team reported "this was missed"
- **Learning Rate**: How quickly the system adapts to feedback

#### **What This Means for Your Community**
- The system learns your community's unique language and communication style
- Over time, it should become better at distinguishing real crises from jokes, gaming references, or casual expressions
- Your corrections directly improve the system for everyone

### **Testing Suite Integration**

Shows results from comprehensive system testing:

#### **Goal Achievement**
- **Pass Rate**: Percentage of tests currently passing
- **Target Achievement**: How close you are to testing goals
- **Performance Trends**: Whether test performance is improving or declining

#### **Recent Test Results**
- **Comprehensive Tests**: Results from the full 350-phrase test suite
- **Quick Validation**: Results from rapid 10-phrase sanity checks
- **Failure Analysis**: Detailed breakdown of any failing tests

#### **What Testing Tells You**
- High pass rates (>90%) indicate the system is working reliably
- Declining performance might indicate system drift or configuration issues
- Specific test failures can help identify what needs attention

---

## 📈 Using the Charts and Visualizations

### **Crisis Trends Chart**

**What it shows**: Timeline of crisis detections over the last 24 hours

**How to read it**:
- X-axis: Time (hourly intervals)
- Y-axis: Number of crisis detections
- Colors: Red (high), Yellow (medium), Green (low crisis levels)

**What to look for**:
- **Normal patterns**: Some communities have predictable busy hours
- **Unusual spikes**: Might indicate community stress or system sensitivity issues
- **Flat lines**: Could mean quiet periods or system problems

**Interactive features**:
- Hover over data points for exact numbers
- Click legend items to show/hide crisis levels
- Charts update automatically every minute

### **Learning Progress Chart**

**What it shows**: How the AI system's accuracy improves over time

**How to read it**:
- X-axis: Time (daily intervals)
- Y-axis: Accuracy percentage
- Line trend: Overall improvement direction

**What to look for**:
- **Upward trends**: System is learning and improving
- **Plateaus**: System has reached stable performance
- **Downward trends**: May indicate need for recalibration

### **Service Performance Charts**

**What they show**: Response times and availability for each service

**Why this matters**:
- Slow response times might affect crisis response speed
- Service interruptions could mean missed crisis situations
- Trends help predict when maintenance might be needed

---

## 🔧 Interactive Features

### **Real-Time Updates**

**What happens automatically**:
- Charts refresh every 30 seconds with new data
- Service status indicators update every minute
- Alert notifications appear immediately for critical issues

**Manual refresh options**:
- Click the refresh button to force immediate update
- Page automatically recovers from temporary connection issues

### **Time Range Selection**

**Available views**:
- **Last Hour**: Detailed minute-by-minute view
- **Last 24 Hours**: Standard overview (default)
- **Last 7 Days**: Weekly patterns and trends
- **Last 30 Days**: Monthly analysis and longer-term trends

**How to change**: Use the time range selector above the charts

### **Data Export**

**What you can export**:
- Crisis detection data (CSV format)
- Learning statistics (JSON format) 
- Testing results (CSV format)
- Service performance metrics (CSV format)

**How to export**:
1. Click the "Export Data" button
2. Select the data type and date range
3. Choose format (CSV for spreadsheets, JSON for technical analysis)
4. Download will start automatically

**Uses for exported data**:
- Create custom reports for leadership
- Analyze trends in external tools
- Archive data for compliance purposes
- Share anonymized statistics with other communities

---

## 🚨 Understanding Alerts and Warnings

### **System Alerts**

#### **Service Down Alerts**
- **Appearance**: Red banner at top of dashboard
- **Meaning**: Critical service is offline
- **Action needed**: Contact technical support immediately
- **Impact**: Crisis detection may be impaired

#### **Performance Warnings**
- **Appearance**: Yellow notification box
- **Meaning**: Service is slow but functional
- **Action needed**: Monitor situation, may resolve automatically
- **Impact**: Slight delays in crisis response

#### **Data Staleness Warnings**
- **Appearance**: Orange timestamp indicators
- **Meaning**: Data hasn't updated recently
- **Action needed**: Refresh page, check network connection
- **Impact**: Dashboard may not show current status

### **Crisis Detection Alerts**

#### **Unusual Pattern Alerts**
- **Trigger**: Sudden spike in crisis detections
- **Possible causes**: Community event, system sensitivity change, actual crisis situation
- **Recommended action**: Review recent Discord activity, check with other team members

#### **System Silence Alerts**
- **Trigger**: No crisis detections for extended period (unusual for your community)
- **Possible causes**: System malfunction, very quiet community period
- **Recommended action**: Verify system is working by checking test messages

#### **Learning System Alerts**
- **Trigger**: Accuracy dropping or learning rate declining
- **Possible causes**: Inconsistent feedback, system drift, community language evolution
- **Recommended action**: Review recent team corrections for consistency

---

## 👥 Team Collaboration Features

### **Role-Based Access**

#### **Observer Role** (Default)
- View all dashboard data and charts
- Export data for analysis
- Cannot modify settings or trigger tests

#### **Moderator Role**
- All Observer capabilities
- Trigger manual testing
- Access detailed failure analysis
- View team activity logs

#### **Administrator Role**
- All Moderator capabilities
- Manage team member access
- Configure alert settings
- Access system logs and diagnostics

### **Activity Logging**

**What's logged**:
- Dashboard access and usage
- Data exports and report generation
- Manual test triggering
- Settings changes (admin only)

**Why this matters**:
- Helps track team coordination
- Provides audit trail for compliance
- Identifies training needs

### **Team Notifications**

**Types of notifications**:
- Critical system alerts
- Weekly performance summaries
- Monthly trend reports
- System maintenance announcements

**How to receive notifications**:
- In-dashboard notification center
- Email alerts (if configured)
- Discord announcements (if integrated)

---

## 📱 Mobile and Remote Access

### **Mobile Browser Support**

**Supported devices**:
- iOS Safari (iPhone/iPad)
- Android Chrome
- Mobile Edge, Firefox

**Mobile features**:
- Responsive design adapts to screen size
- Touch-friendly interactive elements
- Simplified navigation for smaller screens
- All core functionality available

**Mobile limitations**:
- Some detailed charts may be harder to read
- Data export requires desktop browser for large files
- Advanced features may require horizontal orientation

### **Remote Access**

**VPN Requirements**:
- Must be connected to organization VPN
- Network access to 10.20.30.16 subnet required
- Standard HTTPS port (443) must be open

**Security considerations**:
- Always use HTTPS (secure) connection
- Log out when finished, especially on shared devices
- Report suspicious activity or unauthorized access attempts

---

## 🛠️ Troubleshooting for Team Members

### **Common Issues and Solutions**

#### **"Dashboard won't load"**
1. Check internet connection
2. Verify VPN connection (if remote)
3. Try different browser
4. Clear browser cache and cookies
5. Contact technical support if problem persists

#### **"Charts aren't updating"**
1. Refresh the page (Ctrl+F5 or Cmd+Shift+R)
2. Check if timestamp is recent
3. Verify service status indicators are green
4. Wait 2-3 minutes for automatic recovery
5. Report persistent issues to tech support

#### **"Can't export data"**
1. Ensure popup blocker is disabled
2. Try smaller date range
3. Use Chrome or Firefox if using Internet Explorer
4. Check available disk space
5. Contact administrator for large exports

#### **"See 'Certificate Error' or 'Not Secure' warnings"**
1. This is normal for internal tools
2. Click "Advanced" then "Proceed to site"
3. Add security exception if prompted
4. Contact IT if you're uncomfortable proceeding

### **Performance Tips**

#### **For Best Experience**:
- Use Chrome, Firefox, or Edge (avoid Internet Explorer)
- Keep only necessary browser tabs open
- Refresh page if it's been open for several hours
- Use wired internet connection if possible when remote

#### **If Dashboard is Slow**:
- Check if other team members are experiencing issues
- Try accessing during off-peak hours
- Close other bandwidth-intensive applications
- Report persistent performance issues

### **When to Contact Support**

#### **Immediate attention needed**:
- All service indicators are red
- Crisis detection appears to have stopped completely
- Dashboard shows error messages
- Suspicious activity or security concerns

#### **Report within 24 hours**:
- Consistent performance issues
- Unusual patterns in crisis detection
- Missing data or reports
- Questions about data interpretation

#### **General questions**:
- Training requests
- Feature suggestions
- Data analysis help
- Best practices questions

---

## 📚 Best Practices for Crisis Response Teams

### **Daily Routine**

#### **Start of Shift**:
1. Check dashboard service status (all green)
2. Review overnight crisis detection activity
3. Check for any system alerts or notifications
4. Verify learning system is adapting normally

#### **During Shift**:
1. Monitor real-time updates periodically
2. Report false positives/negatives promptly
3. Note any unusual community activity
4. Coordinate with other team members on significant events

#### **End of Shift**:
1. Document any significant incidents
2. Report system issues to next shift
3. Export data if needed for reports
4. Note recommendations for system improvements

### **Weekly Activities**

#### **Team Coordination**:
- Review weekly performance summary
- Discuss any patterns or concerns
- Coordinate feedback on false positives/negatives
- Plan any needed training or process improvements

#### **Data Analysis**:
- Export weekly data for trend analysis
- Compare performance to previous weeks
- Identify areas for system improvement
- Document lessons learned

### **Monthly Activities**

#### **Performance Review**:
- Generate monthly performance reports
- Analyze long-term trends
- Review learning system effectiveness
- Plan system optimizations

#### **Team Training**:
- Review any new features or changes
- Share best practices and lessons learned
- Train new team members
- Update procedures as needed

---

## 🎯 Understanding Your Impact

### **How Your Work Improves the System**

#### **Every Correction Matters**:
- When you report a false positive, the system learns to be less sensitive to that pattern
- When you report a missed crisis, the system learns to watch for similar language
- Your feedback directly improves detection accuracy for your community

#### **Community-Specific Learning**:
- The system learns your community's unique slang and expressions
- Gaming references, memes, and inside jokes are gradually filtered out
- Real crisis language becomes more accurately identified

#### **Measurable Improvements**:
- Watch the accuracy percentages increase over time
- See false positive rates decrease as the system learns
- Observe faster, more appropriate responses to real crisis situations

### **Success Metrics to Track**

#### **Detection Accuracy**:
- **Target**: >95% accuracy rate
- **Trend**: Steady improvement over time
- **Your impact**: Direct correlation with team feedback quality

#### **Response Time**:
- **Target**: <30 seconds for crisis identification
- **Trend**: Consistent or improving performance
- **Your impact**: System stability affects response reliability

#### **Community Safety**:
- **Measure**: Successful interventions and support provided
- **Trend**: Improved crisis outcomes and community wellbeing
- **Your impact**: Better detection leads to better support

---

## 📞 Getting Help and Support

### **Support Resources**

#### **Documentation**:
- **This Team Guide**: Day-to-day usage and best practices
- **Deployment Guide**: Technical setup information (for IT)
- **API Documentation**: Technical integration details (for developers)
- **Troubleshooting Guide**: Common issues and solutions

#### **Community Support**:
- **Discord #tech-support**: Real-time help from community and developers
- **GitHub Issues**: Bug reports and feature requests
- **Team Meetings**: Regular check-ins and training sessions

### **Contact Information**

#### **Emergency Support** (System Down):
- Discord: Ping @tech-lead role
- Emergency contact: [Contact information]
- Escalation: [Contact information]

#### **General Support**:
- Discord: #tech-support channel
- GitHub: https://github.com/The-Alphabet-Cartel/ash-dash/issues
- Email: [Support email if available]

#### **Training and Best Practices**:
- Schedule training: [Process for requesting training]
- Best practices questions: #crisis-response channel
- Process improvements: [Process for suggesting improvements]

---

## 🔄 Updates and Changes

### **How You'll Be Notified**

#### **System Updates**:
- Dashboard notifications for new features
- Discord announcements for major changes
- Email notifications for critical updates
- Version information displayed in dashboard footer

#### **Process Changes**:
- Team meeting discussions
- Updated documentation
- Training sessions for new procedures

### **Providing Feedback**

#### **Feature Requests**:
- Use GitHub Issues for new feature ideas
- Discuss in team meetings
- Vote on community priorities

#### **Bug Reports**:
- Report via Discord #tech-support
- Include specific steps to reproduce
- Provide screenshots when helpful

#### **Process Improvements**:
- Suggest during team meetings
- Document what's working well and what isn't
- Share ideas with other team members

---

## 🎓 Training and Onboarding

### **New Team Member Checklist**

#### **Week 1: Getting Familiar**
- [ ] Access dashboard successfully
- [ ] Understand service status indicators
- [ ] Know how to read crisis detection metrics
- [ ] Practice exporting data
- [ ] Complete basic troubleshooting

#### **Week 2: Active Monitoring**
- [ ] Monitor dashboard during actual shifts
- [ ] Report first false positive/negative
- [ ] Understand learning system impact
- [ ] Coordinate with experienced team members

#### **Week 3: Advanced Features**
- [ ] Use all time range options
- [ ] Generate and analyze reports
- [ ] Understand testing suite results
- [ ] Participate in team performance review

#### **Week 4: Full Proficiency**
- [ ] Train another new team member
- [ ] Suggest process improvements
- [ ] Handle routine issues independently
- [ ] Contribute to team best practices

### **Ongoing Training Opportunities**

#### **Monthly Team Sessions**:
- New feature demonstrations
- Data analysis workshops
- Best practices sharing
- Q&A with technical team

#### **Quarterly Reviews**:
- Performance assessment
- System effectiveness evaluation
- Process improvement planning
- Advanced feature training

---

*This team guide is part of the ash-dash v2.1 documentation suite. For technical implementation details, see the other guides in the `/docs` directory. For real-time support, join us in [The Alphabet Cartel Discord](https://discord.gg/alphabetcartel).*