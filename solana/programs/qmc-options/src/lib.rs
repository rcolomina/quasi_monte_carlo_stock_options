// Solana Options Protocol using QMC Pricing
// Anchor framework for Solana smart contracts

use anchor_lang::prelude::*;

declare_id!("Fg6PaFpoGXkYsidMpWTK6W2BeZ7FEfcYkg476zPFsLnS"); // Replace with your program ID

#[program]
pub mod qmc_options {
    use super::*;

    /// Initialize the protocol
    pub fn initialize(ctx: Context<Initialize>) -> Result<()> {
        let protocol = &mut ctx.accounts.protocol;
        protocol.authority = ctx.accounts.authority.key();
        protocol.total_volume = 0;
        protocol.total_options_created = 0;
        Ok(())
    }

    /// Update oracle price (called by off-chain crank)
    pub fn update_oracle_price(
        ctx: Context<UpdateOraclePrice>,
        option_id: String,
        price: u64,      // Price with 6 decimals (e.g., 1.23 = 1_230_000)
        delta: i64,      // Delta with 6 decimals
        timestamp: i64,
        model_type: String,
    ) -> Result<()> {
        require!(
            ctx.accounts.authority.key() == ctx.accounts.protocol.authority,
            ErrorCode::Unauthorized
        );

        let oracle = &mut ctx.accounts.oracle;
        oracle.option_id = option_id;
        oracle.price = price;
        oracle.delta = delta;
        oracle.last_update = timestamp;
        oracle.model_type = model_type;

        emit!(PriceUpdated {
            option_id: oracle.option_id.clone(),
            price,
            delta,
            timestamp,
        });

        Ok(())
    }

    /// Create option contract
    pub fn create_option(
        ctx: Context<CreateOption>,
        strike_price: u64,
        expiry: i64,
        option_type: OptionType,
        amount: u64,
    ) -> Result<()> {
        let option = &mut ctx.accounts.option;
        let protocol = &mut ctx.accounts.protocol;

        option.writer = ctx.accounts.writer.key();
        option.underlying_asset = ctx.accounts.underlying_mint.key();
        option.strike_price = strike_price;
        option.expiry = expiry;
        option.option_type = option_type;
        option.amount = amount;
        option.is_exercised = false;
        option.created_at = Clock::get()?.unix_timestamp;

        protocol.total_options_created += 1;

        emit!(OptionCreated {
            option_id: option.key(),
            writer: option.writer,
            strike_price,
            expiry,
            option_type,
            amount,
        });

        Ok(())
    }

    /// Exercise option at expiry
    pub fn exercise_option(ctx: Context<ExerciseOption>) -> Result<()> {
        let option = &mut ctx.accounts.option;
        let current_time = Clock::get()?.unix_timestamp;

        // Check expiry
        require!(current_time >= option.expiry, ErrorCode::NotExpired);
        require!(!option.is_exercised, ErrorCode::AlreadyExercised);

        // Fetch current price from Pyth oracle
        let pyth_price = get_pyth_price(&ctx.accounts.pyth_account)?;

        // Calculate payoff
        let payoff = match option.option_type {
            OptionType::Call => {
                if pyth_price > option.strike_price {
                    option.amount * (pyth_price - option.strike_price) / 1_000_000
                } else {
                    0
                }
            }
            OptionType::Put => {
                if option.strike_price > pyth_price {
                    option.amount * (option.strike_price - pyth_price) / 1_000_000
                } else {
                    0
                }
            }
        };

        if payoff > 0 {
            // Transfer collateral to option holder
            // (Simplified - actual implementation uses token transfers)
            option.is_exercised = true;

            emit!(OptionExercised {
                option_id: option.key(),
                payoff,
                final_price: pyth_price,
            });
        }

        Ok(())
    }

    /// Buy option from liquidity pool (AMM-style)
    pub fn buy_option(
        ctx: Context<BuyOption>,
        amount: u64,
        max_premium: u64,
    ) -> Result<()> {
        let oracle = &ctx.accounts.oracle;
        let pool = &mut ctx.accounts.liquidity_pool;

        // Premium = QMC computed price + fee
        let base_premium = oracle.price;
        let fee = base_premium / 100; // 1% protocol fee
        let total_premium = base_premium + fee;

        require!(total_premium <= max_premium, ErrorCode::SlippageExceeded);

        // Transfer premium from buyer to pool
        // (Token transfer logic here)

        pool.total_volume += total_premium;

        emit!(OptionPurchased {
            buyer: ctx.accounts.buyer.key(),
            premium: total_premium,
            amount,
        });

        Ok(())
    }
}

// Account structures
#[account]
pub struct Protocol {
    pub authority: Pubkey,
    pub total_volume: u64,
    pub total_options_created: u64,
}

#[account]
pub struct PriceOracle {
    pub option_id: String,
    pub price: u64,           // QMC computed price
    pub delta: i64,           // Delta for risk management
    pub last_update: i64,
    pub model_type: String,   // "heston", "merton", etc.
}

#[account]
pub struct OptionContract {
    pub writer: Pubkey,
    pub underlying_asset: Pubkey,
    pub strike_price: u64,
    pub expiry: i64,
    pub option_type: OptionType,
    pub amount: u64,
    pub is_exercised: bool,
    pub created_at: i64,
}

#[account]
pub struct LiquidityPool {
    pub total_liquidity: u64,
    pub total_volume: u64,
    pub asset: Pubkey,
}

// Enums
#[derive(AnchorSerialize, AnchorDeserialize, Clone, PartialEq, Eq)]
pub enum OptionType {
    Call,
    Put,
}

// Context structs
#[derive(Accounts)]
pub struct Initialize<'info> {
    #[account(init, payer = authority, space = 8 + 32 + 8 + 8)]
    pub protocol: Account<'info, Protocol>,
    #[account(mut)]
    pub authority: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdateOraclePrice<'info> {
    #[account(mut)]
    pub oracle: Account<'info, PriceOracle>,
    pub protocol: Account<'info, Protocol>,
    pub authority: Signer<'info>,
}

#[derive(Accounts)]
pub struct CreateOption<'info> {
    #[account(init, payer = writer, space = 8 + 200)]
    pub option: Account<'info, OptionContract>,
    #[account(mut)]
    pub writer: Signer<'info>,
    pub underlying_mint: Account<'info, anchor_spl::token::Mint>,
    #[account(mut)]
    pub protocol: Account<'info, Protocol>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct ExerciseOption<'info> {
    #[account(mut)]
    pub option: Account<'info, OptionContract>,
    pub holder: Signer<'info>,
    /// CHECK: Pyth price account
    pub pyth_account: AccountInfo<'info>,
}

#[derive(Accounts)]
pub struct BuyOption<'info> {
    pub oracle: Account<'info, PriceOracle>,
    #[account(mut)]
    pub liquidity_pool: Account<'info, LiquidityPool>,
    #[account(mut)]
    pub buyer: Signer<'info>,
}

// Events
#[event]
pub struct PriceUpdated {
    pub option_id: String,
    pub price: u64,
    pub delta: i64,
    pub timestamp: i64,
}

#[event]
pub struct OptionCreated {
    pub option_id: Pubkey,
    pub writer: Pubkey,
    pub strike_price: u64,
    pub expiry: i64,
    pub option_type: OptionType,
    pub amount: u64,
}

#[event]
pub struct OptionExercised {
    pub option_id: Pubkey,
    pub payoff: u64,
    pub final_price: u64,
}

#[event]
pub struct OptionPurchased {
    pub buyer: Pubkey,
    pub premium: u64,
    pub amount: u64,
}

// Error codes
#[error_code]
pub enum ErrorCode {
    #[msg("Unauthorized")]
    Unauthorized,
    #[msg("Option not expired")]
    NotExpired,
    #[msg("Option already exercised")]
    AlreadyExercised,
    #[msg("Slippage tolerance exceeded")]
    SlippageExceeded,
}

// Helper functions
fn get_pyth_price(pyth_account: &AccountInfo) -> Result<u64> {
    // Parse Pyth price account
    // (Actual implementation uses pyth-sdk-solana)
    Ok(100_000_000) // Placeholder
}
