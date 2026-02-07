-- AI Body Measurement System - Database Schema
-- PostgreSQL Database Schema

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- ============================================
-- USERS TABLE
-- ============================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    date_of_birth DATE,
    phone_number VARCHAR(20),
    preferred_unit VARCHAR(10) DEFAULT 'cm' CHECK (preferred_unit IN ('cm', 'inches')),
    preferred_language VARCHAR(10) DEFAULT 'en',
    is_active BOOLEAN DEFAULT TRUE,
    is_admin BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Index for faster email lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_gender ON users(gender);

-- ============================================
-- MEASUREMENT PROFILES TABLE
-- ============================================
CREATE TABLE measurement_profiles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    profile_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    relationship VARCHAR(50), -- 'self', 'spouse', 'child', etc.
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_profiles_user_id ON measurement_profiles(user_id);

-- ============================================
-- MEASUREMENTS TABLE (Gender-Specific)
-- ============================================
CREATE TABLE measurements (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    profile_id UUID REFERENCES measurement_profiles(id) ON DELETE SET NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female')),
    
    -- Common measurements (in cm)
    height DECIMAL(6,2),
    waist DECIMAL(6,2),
    hip DECIMAL(6,2),
    shoulder_width DECIMAL(6,2),
    arm_length DECIMAL(6,2),
    sleeve_length DECIMAL(6,2),
    neck DECIMAL(6,2),
    thigh DECIMAL(6,2),
    calf DECIMAL(6,2),
    
    -- Male-specific measurements
    chest DECIMAL(6,2), -- For males
    inseam DECIMAL(6,2),
    outseam DECIMAL(6,2),
    
    -- Female-specific measurements
    bust DECIMAL(6,2), -- For females
    under_bust DECIMAL(6,2),
    
    -- Confidence scores (0-100)
    height_confidence DECIMAL(5,2),
    chest_bust_confidence DECIMAL(5,2),
    waist_confidence DECIMAL(5,2),
    hip_confidence DECIMAL(5,2),
    overall_confidence DECIMAL(5,2),
    
    -- Metadata
    measurement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    processing_time_ms INTEGER,
    ai_model_version VARCHAR(50),
    reference_object VARCHAR(50), -- 'credit_card', 'a4_sheet', etc.
    
    -- Status
    status VARCHAR(20) DEFAULT 'completed' CHECK (status IN ('processing', 'completed', 'flagged', 'rejected')),
    flagged_reason TEXT,
    admin_reviewed BOOLEAN DEFAULT FALSE,
    admin_notes TEXT,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_measurements_user_id ON measurements(user_id);
CREATE INDEX idx_measurements_profile_id ON measurements(profile_id);
CREATE INDEX idx_measurements_date ON measurements(measurement_date);
CREATE INDEX idx_measurements_status ON measurements(status);

-- ============================================
-- SIZE RECOMMENDATIONS TABLE
-- ============================================
CREATE TABLE size_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    measurement_id UUID NOT NULL REFERENCES measurements(id) ON DELETE CASCADE,
    brand_id UUID REFERENCES size_charts(id) ON DELETE SET NULL,
    
    -- Recommended sizes
    general_size VARCHAR(10), -- 'XS', 'S', 'M', 'L', 'XL', 'XXL'
    numeric_size VARCHAR(10), -- '32', '34', '36', etc.
    
    -- Size by region
    us_size VARCHAR(10),
    uk_size VARCHAR(10),
    eu_size VARCHAR(10),
    asia_size VARCHAR(10),
    
    -- Fit preference
    fit_preference VARCHAR(20) CHECK (fit_preference IN ('slim', 'regular', 'loose')),
    
    -- Confidence
    recommendation_confidence DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_size_rec_measurement_id ON size_recommendations(measurement_id);

-- ============================================
-- SIZE CHARTS TABLE (Brand-Specific)
-- ============================================
CREATE TABLE size_charts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    brand_name VARCHAR(100) NOT NULL,
    gender VARCHAR(10) NOT NULL CHECK (gender IN ('male', 'female', 'unisex')),
    category VARCHAR(50), -- 'shirts', 'pants', 'dresses', etc.
    
    -- Size mappings (JSON format for flexibility)
    size_data JSONB NOT NULL,
    -- Example: {"S": {"chest": [86, 91], "waist": [71, 76]}, "M": {...}}
    
    region VARCHAR(10) DEFAULT 'US', -- 'US', 'UK', 'EU', 'Asia'
    is_active BOOLEAN DEFAULT TRUE,
    version INTEGER DEFAULT 1,
    
    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_size_charts_brand ON size_charts(brand_name);
CREATE INDEX idx_size_charts_gender ON size_charts(gender);

-- ============================================
-- USER FEEDBACK TABLE
-- ============================================
CREATE TABLE user_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    measurement_id UUID REFERENCES measurements(id) ON DELETE CASCADE,
    
    -- Feedback type
    feedback_type VARCHAR(50) CHECK (feedback_type IN ('measurement_accuracy', 'size_recommendation', 'general')),
    
    -- Ratings (1-5)
    accuracy_rating INTEGER CHECK (accuracy_rating BETWEEN 1 AND 5),
    ease_of_use_rating INTEGER CHECK (ease_of_use_rating BETWEEN 1 AND 5),
    
    -- Comments
    comments TEXT,
    
    -- Actual size purchased (if applicable)
    actual_size_purchased VARCHAR(10),
    fit_result VARCHAR(20) CHECK (fit_result IN ('too_small', 'perfect', 'too_large')),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_feedback_user_id ON user_feedback(user_id);
CREATE INDEX idx_feedback_measurement_id ON user_feedback(measurement_id);

-- ============================================
-- AUDIT LOGS TABLE
-- ============================================
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    action VARCHAR(100) NOT NULL,
    entity_type VARCHAR(50), -- 'user', 'measurement', 'size_chart', etc.
    entity_id UUID,
    old_values JSONB,
    new_values JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_audit_logs_user_id ON audit_logs(user_id);
CREATE INDEX idx_audit_logs_created_at ON audit_logs(created_at);
CREATE INDEX idx_audit_logs_action ON audit_logs(action);

-- ============================================
-- SYSTEM ANALYTICS TABLE
-- ============================================
CREATE TABLE system_analytics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    date DATE NOT NULL,
    
    -- User metrics
    total_users INTEGER DEFAULT 0,
    new_users INTEGER DEFAULT 0,
    active_users INTEGER DEFAULT 0,
    
    -- Measurement metrics
    total_measurements INTEGER DEFAULT 0,
    successful_measurements INTEGER DEFAULT 0,
    flagged_measurements INTEGER DEFAULT 0,
    
    -- Performance metrics
    avg_processing_time_ms INTEGER,
    avg_confidence_score DECIMAL(5,2),
    
    -- AI metrics
    model_version VARCHAR(50),
    accuracy_rate DECIMAL(5,2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    UNIQUE(date)
);

CREATE INDEX idx_analytics_date ON system_analytics(date);

-- ============================================
-- TRIGGERS FOR UPDATED_AT
-- ============================================

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Apply trigger to tables
CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON users
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON measurement_profiles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_measurements_updated_at BEFORE UPDATE ON measurements
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_size_charts_updated_at BEFORE UPDATE ON size_charts
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================
-- SAMPLE DATA (Optional - for testing)
-- ============================================

-- Insert sample size chart for a brand
INSERT INTO size_charts (brand_name, gender, category, size_data) VALUES
('Generic Brand', 'male', 'shirts', '{
    "S": {"chest": [86, 91], "waist": [71, 76], "shoulder": [42, 44]},
    "M": {"chest": [91, 97], "waist": [76, 81], "shoulder": [44, 46]},
    "L": {"chest": [97, 102], "waist": [81, 86], "shoulder": [46, 48]},
    "XL": {"chest": [102, 107], "waist": [86, 91], "shoulder": [48, 50]},
    "XXL": {"chest": [107, 112], "waist": [91, 97], "shoulder": [50, 52]}
}'::jsonb),
('Generic Brand', 'female', 'dresses', '{
    "XS": {"bust": [76, 81], "waist": [61, 66], "hip": [86, 91]},
    "S": {"bust": [81, 86], "waist": [66, 71], "hip": [91, 97]},
    "M": {"bust": [86, 91], "waist": [71, 76], "hip": [97, 102]},
    "L": {"bust": [91, 97], "waist": [76, 81], "hip": [102, 107]},
    "XL": {"bust": [97, 102], "waist": [81, 86], "hip": [107, 112]},
    "XXL": {"bust": [102, 107], "waist": [86, 91], "hip": [112, 117]}
}'::jsonb);

-- ============================================
-- VIEWS FOR COMMON QUERIES
-- ============================================

-- View for user measurement history
CREATE VIEW user_measurement_history AS
SELECT 
    m.id,
    m.user_id,
    u.email,
    u.gender,
    m.height,
    CASE 
        WHEN u.gender = 'male' THEN m.chest
        WHEN u.gender = 'female' THEN m.bust
    END as chest_bust,
    m.waist,
    m.hip,
    m.overall_confidence,
    m.measurement_date,
    m.status
FROM measurements m
JOIN users u ON m.user_id = u.id
ORDER BY m.measurement_date DESC;

-- View for analytics dashboard
CREATE VIEW analytics_dashboard AS
SELECT 
    COUNT(DISTINCT u.id) as total_users,
    COUNT(DISTINCT CASE WHEN u.created_at >= CURRENT_DATE - INTERVAL '30 days' THEN u.id END) as new_users_30d,
    COUNT(DISTINCT m.id) as total_measurements,
    COUNT(DISTINCT CASE WHEN m.measurement_date >= CURRENT_DATE - INTERVAL '30 days' THEN m.id END) as measurements_30d,
    AVG(m.processing_time_ms) as avg_processing_time,
    AVG(m.overall_confidence) as avg_confidence,
    COUNT(CASE WHEN m.status = 'flagged' THEN 1 END) as flagged_count
FROM users u
LEFT JOIN measurements m ON u.id = m.user_id;

-- ============================================
-- COMMENTS
-- ============================================

COMMENT ON TABLE users IS 'Stores user account information with gender-specific settings';
COMMENT ON TABLE measurements IS 'Stores body measurements with gender-specific parameters';
COMMENT ON TABLE size_charts IS 'Brand-specific size charts for size recommendations';
COMMENT ON TABLE user_feedback IS 'User feedback on measurement accuracy and size recommendations';
COMMENT ON TABLE audit_logs IS 'Audit trail for all system actions';

-- End of schema
